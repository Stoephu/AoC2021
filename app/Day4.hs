import Debug.Trace

main :: IO ()
main = do
    contents <- readFile "inputs/Day4.txt"
    let listOfLine = lines contents
    let replacerCom = replace (== ',') ' '
    let pulls = map read $ wordsWhen replacerCom $ head listOfLine :: [Int]
    let boardints = map (map read . wordsWhen replacerCom) (tail $ tail listOfLine) :: [[Int]]
    print pulls
    print $ play (map addTransposeBoard $ groupBoards boardints) pulls 
    print $ play2 (map addTransposeBoard $ groupBoards boardints) pulls 
    
    -- part due


wordsWhen :: (String -> String) -> String ->  [String]
wordsWhen repl string = words modifiedString
    where modifiedString = repl string

replace :: (Char -> Bool) -> Char -> String -> String
replace _ _ [] = []
replace con rep (c:cs) = if con c then rep:replace con rep cs else c:replace con rep cs

groupBoards :: [[Int]] -> [[[Int]]]
groupBoards [] = []
groupBoards xs = take 5 xs : groupBoards (drop 6 xs)

addTransposeBoard :: [[Int]] -> [[Int]]
addTransposeBoard board = merge board transposed
    where transposed = transposeBoard board

transposeBoard :: [[Int]] -> [[Int]]
transposeBoard ([]:_) = []
transposeBoard board = map head board : transposeBoard (map tail board) 

pop :: Int -> [Int] -> [Int]
pop _ [] = []
pop y (x:xs) = if x == y then xs else x: pop y xs

merge :: [a] -> [a] -> [a]
merge [] ys = ys
merge (x:xs) ys = x:merge ys xs

play :: [[[Int]]] -> [Int] -> Int
play boards (p:pulls) = if null winningBoards then play nextBoards pulls else div (sum $ map sum (head winningBoards) ) 2 * p
    where   nextBoards = map (map (pop p)) boards
            winningBoards = filter (any null) nextBoards
play _ _ = error "go away"

play2 :: [[[Int]]] -> [Int] -> Int
play2 boards (p:pulls) = trace (show p ++ " \n " ++ show currentLosingBoards ++"\n" ++ show nextLosingBoards ) (if (length currentLosingBoards == 1) && null nextLosingBoards then div (sum $ map sum (head currentLosingBoards) ) 2 * p - p * p else play2 nextBoards pulls )
    where   nextBoards = map (map (pop p)) boards
            currentLosingBoards = filter (not . any null) boards
            nextLosingBoards = filter (not . any null) nextBoards
play2 _ _ = error "go away"
