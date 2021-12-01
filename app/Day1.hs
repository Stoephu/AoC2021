import System.IO


main :: IO ()
main = do
    contents <- readFile "inputs/day1.txt"
    let numbers = parseContent contents
    let result = neighbourIncrease 0 numbers
    let resultString = show result
    putStr resultString
    -- part deux
    let triplenumbers = tripledepths numbers
    print triplenumbers
    let result2 = neighbourIncrease 0 triplenumbers
    print result2

parseContent :: [Char] -> [Int]
parseContent contents = map read (lines contents)

neighbourIncrease :: Int -> [Int] -> Int
neighbourIncrease i [x] = i
neighbourIncrease i (x:xs) = if x < head xs then neighbourIncrease (i + 1) xs else neighbourIncrease i xs

tripledepths :: [Int] -> [Int]
tripledepths xs = [a + b + c | (a,b,c) <- threezip first second third]
    where   third = tail (tail xs)
            second = init (tail xs)
            first = init (init xs)

threezip :: [Int] -> [Int] -> [Int] -> [(Int,Int,Int)]
threezip [] [] [] = []
threezip (a:as) (b:bs) (c:cs) = (a,b,c) : threezip as bs cs