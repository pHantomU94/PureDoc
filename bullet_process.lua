-- 1. 定义核心逻辑：把所有含“软回车”的段落，切碎成多个“硬回车”段落
-- 这个函数现在是通用的，谁都可以调
local function split_para_by_softbreak(blk)
    -- 安全检查：如果不是段落，直接返回
    if blk.t ~= "Para" and blk.t ~= "Plain" then return {blk} end
  
    local result_blocks = {}
    local current_inlines = {}
  
    for _, inline in ipairs(blk.content) do
        -- 核心：遇到 SoftBreak (软回车) 或 LineBreak (强行换行) 就切断
        if inline.t == "SoftBreak" or inline.t == "LineBreak" then
            if #current_inlines > 0 then
                table.insert(result_blocks, pandoc.Para(current_inlines))
                current_inlines = {}
            end
        else
            table.insert(current_inlines, inline)
        end
    end
    
    -- 收尾：处理最后剩下的文字
    if #current_inlines > 0 then
        table.insert(result_blocks, pandoc.Para(current_inlines))
    end
    
    return result_blocks
end

-- 2. 新增：全局段落过滤器 (解决问题2)
-- 只要是段落，不管是列表里的还是外面的，统统过一遍切断逻辑
function Para(el)
    return split_para_by_softbreak(el)
end

-- 3. 处理有序列表 (保留 1. 2. 3.)
function OrderedList(el)
    local result = pandoc.List()
    for i, item in ipairs(el.content) do
        -- 手动加数字前缀 (例如 "1. ")
        if item[1] and (item[1].t == "Para" or item[1].t == "Plain") then
            local prefix = i .. ". "
            table.insert(item[1].content, 1, pandoc.Str(prefix))
        end
        
        -- 平铺内容
        for _, block in ipairs(item) do
            -- 注意：这里依然要调用切分逻辑，处理列表项内部的换行
            local split_blocks = split_para_by_softbreak(block)
            for _, b in ipairs(split_blocks) do
                result:insert(b)
            end
        end
    end
    return result
end

-- 4. 处理无序列表 (解决问题1：直接忽略符号)
function BulletList(el)
    local result = pandoc.List()
    for _, item in ipairs(el.content) do
        -- 【关键修改】这里不再插入 pandoc.Str("• ") 
        -- 纯粹地把内容提取出来，不做任何符号添加
        
        for _, block in ipairs(item) do
            local split_blocks = split_para_by_softbreak(block)
            for _, b in ipairs(split_blocks) do
                result:insert(b)
            end
        end
    end
    return result
end