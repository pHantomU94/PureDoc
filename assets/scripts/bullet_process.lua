-- strip_lists.lua (扩展版：支持有序列表三种模式)

-- 1. 辅助工具：处理软回车 (保持不变)
local function split_para_by_softbreak(blk)
    if blk.t ~= "Para" and blk.t ~= "Plain" then return {blk} end
    local result_blocks = {}
    local current_inlines = {}
    
    for _, inline in ipairs(blk.content) do
        if inline.t == "SoftBreak" or inline.t == "LineBreak" then
            if #current_inlines > 0 then
                table.insert(result_blocks, pandoc.Para(current_inlines))
                current_inlines = {}
            end
        else
            table.insert(current_inlines, inline)
        end
    end
    
    if #current_inlines > 0 then
        table.insert(result_blocks, pandoc.Para(current_inlines))
    end
    
    return result_blocks
end

-- 2. 核心入口：处理整个文档
function Pandoc(doc)
    -- ============================================================
    -- A. 读取元数据配置
    -- ============================================================
    
    -- 1. 获取无序列表 (Bullet) 配置
    local ignore_bullets = false
    if doc.meta.ignore_bullets then
        if pandoc.utils.stringify(doc.meta.ignore_bullets) == "true" then
            ignore_bullets = true
        end
    end

    -- 2. 获取有序列表 (Ordered) 配置
    -- 选项: "list" (自动列表), "text" (纯文本数字), "none" (无数字)
    local ol_style = "list" -- 默认为自动列表
    if doc.meta.ordered_list_style then
        ol_style = pandoc.utils.stringify(doc.meta.ordered_list_style)
    end

    -- ============================================================
    -- B. 定义过滤器逻辑
    -- ============================================================
    local filter = {
        -- 处理段落（软回车切分）
        Para = function(el)
            return split_para_by_softbreak(el)
        end,

        -- 处理无序列表 (BulletList)
        BulletList = function(el)
            local result = pandoc.List()
            for _, item in ipairs(el.content) do
                -- 核心判断：如果不忽略，就加点；如果忽略(true)，就啥也不加
                if not ignore_bullets then
                    if item[1] and (item[1].t == "Para" or item[1].t == "Plain") then
                        table.insert(item[1].content, 1, pandoc.Str("• "))
                    end
                end
                
                -- 平铺内容 (Flatten)
                for _, block in ipairs(item) do
                    local split_blocks = split_para_by_softbreak(block)
                    for _, b in ipairs(split_blocks) do
                        result:insert(b)
                    end
                end
            end
            return result
        end,

        -- 处理有序列表 (OrderedList)
        OrderedList = function(el)
            -- 模式1: Word 自动列表 (list)
            -- 直接返回 nil，意味着不做任何修改，Pandoc 会把它转为原生的 Word 列表
            -- 注意：Pandoc 依然会递归遍历内部的 Para，所以软回车处理依然生效
            if ol_style == "list" then
                return nil 
            end

            -- 下面是 "text" 或 "none" 模式，都需要把列表拍平 (Flatten)
            local result = pandoc.List()
            
            for i, item in ipairs(el.content) do
                -- 模式2: 纯文本数字 (text)
                -- 只有在 text 模式下，才给第一段加前缀
                if ol_style == "text" then
                    if item[1] and (item[1].t == "Para" or item[1].t == "Plain") then
                        -- 获取当前序号，生成 "1. "
                        local prefix = i .. ". "
                        -- 如果有起始序号设置 (start number)，可以更严谨：
                        -- local num = (el.start or 1) + i - 1
                        -- local prefix = num .. ". "
                        
                        table.insert(item[1].content, 1, pandoc.Str(prefix))
                    end
                end
                
                -- 模式3 (none) 不需要做任何操作，直接跳过上面的 if，进入下面的平铺逻辑

                -- 平铺内容：将列表项里的 Block 提取出来放到结果列表中
                for _, block in ipairs(item) do
                    local split_blocks = split_para_by_softbreak(block)
                    for _, b in ipairs(split_blocks) do
                        result:insert(b)
                    end
                end
            end
            
            return result
        end
    }

    -- C. 带着过滤器遍历整个文档
    return doc:walk(filter)
end