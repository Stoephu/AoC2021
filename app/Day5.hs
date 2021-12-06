import Debug.Trace

main :: IO ()
main = do
    contents <- readFile "inputs/day5.txt"
    let listOfWords = map words $ lines contents
    let tpls = endStart listOfWords
    --print $ show tpls
    let horz = sortHorz tpls 
    --print horz
    let verts = sortVert tpls 
    --print verts
    print "Part 1"
    let merged = merge horz verts
    --print merged
    let coordsHit = concatMap generateCoords merged
    --print coordsHit
    print $ filter (\x -> 1 < snd x) $ getOccurences (uniq coordsHit) coordsHit
    print $ length $ filter (\x -> 1 < snd x) $ getOccurences (uniq coordsHit) coordsHit
    -- part due

merge :: [a] -> [a] -> [a]
merge [] ys = ys
merge (x:xs) ys = x:merge ys xs

endStart :: [[String]] -> [((Int,Int), (Int,Int))]
endStart [] = []
endStart (tup:xs) = ((read  (head x), read  (last x)),(read  (head y), read  (last y))):endStart xs
    where   x = words $ repl $ head tup :: [String]
            y = words $ repl $ last tup :: [String]
            repl = replace (==',') ' '


replace :: (Char -> Bool) -> Char -> String -> String
replace _ _ [] = []
replace con rep (c:cs) = if con c then rep:replace con rep cs else c:replace con rep cs


sortHorz ::  [((Int,Int), (Int,Int))] ->  [((Int,Int), (Int,Int))]
sortHorz [] = []
sortHorz (coords@((a,_),(b,_)):xs) 
    | a == b  = coords : sortHorz xs 
    | otherwise= sortHorz xs 

sortVert :: [((Int,Int), (Int,Int))] ->  [((Int,Int), (Int,Int))]
sortVert [] = []
sortVert (coords@((_,a),(_,b)):xs) 
    | a == b = coords : sortVert xs
    | otherwise = sortVert xs

generateCoords :: ((Int,Int),(Int, Int)) -> [(Int,Int)]
generateCoords ((a1,a2),(b1,b2)) = zipB a b
    where   a = if a1 < b1 then [a1 .. b1] else reverse [b1 .. a1]
            b = if a2 < b2 then [a2 .. b2] else reverse [b2 .. a2]

zipB [a] ls = [(a,l) | l <- ls]
zipB ls [a] = [(l,a) | l <- ls]
zipB hs ls = zip hs ls

getOccurences [] _  = []
getOccurences (u:us) xs = (u, length $ filter (== u) xs):getOccurences us xs

uniq :: Eq a => [a] -> [a]
uniq [] = []
uniq (x:xs) = (if x `elem` xs then id else (x:)) $ uniq xs