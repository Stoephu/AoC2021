import Debug.Trace

main :: IO ()
main = do
    contents <- readFile "inputs/Day3.txt"
    let listOfLine = lines contents
    let gamma = commonBins  listOfLine
    let epsilon = negateBin gamma
    print $  bin2dec (concat gamma) * bin2dec (concat epsilon)
    -- part due
    let temp1 = concat $ search True 0 $ map (map charToString) listOfLine :: String
    print $ bin2dec temp1 
    let temp2 = concat $ search False 0 $ map (map charToString) listOfLine :: String
    print $ bin2dec temp2
    print $ bin2dec temp1 * bin2dec temp2

bin2dec :: [Char] -> Int
bin2dec = foldl (\acc x -> acc*2 + charToInt x) 0

charToString :: Char -> String
charToString =(:[])

charToInt :: Char -> Int
charToInt c = read $ charToString c

transposeStrings :: [String] -> [String] -> [String]
transposeStrings = foldl (\acc newString -> [a ++ b| (a,b) <- zip acc $ map charToString newString]) 

mostCommonBin :: String -> String
mostCommonBin string =  if oneCounts >= half then "1" else "0"
    where   half = fromIntegral (length string) / 2 :: Float
            oneCounts = foldl (\acc x -> if x == '1' then acc + 1 else acc) 0 string

commonBins :: [String] -> [String]
commonBins [] = []
commonBins (x:xs) = map mostCommonBin $ transposeStrings (map charToString x) xs


negateBin :: [String] -> [String]
negateBin [] = []
negateBin ("1":xs) = "0":negateBin xs
negateBin ("0":xs) = "1":negateBin xs
negateBin _ = error "no pattern matched to 0 or 1"


search :: Bool -> Int -> [[String]] -> [String]
search _ _ [] = error " filtered all strings"
search _ _ [x] = trace ("search: " ++ show x) x
search most position strings = trace ("search: " ++ show position ++ " " ++ show mostCommon ++ " " ++ criteria ++ " " ++ show strings) $ search most (position + 1) $ filter (\x -> criteria == x !! position) strings
    where   mostCommon = commonBins (map concat strings)
            leastCommon = negateBin (commonBins (map concat strings))
            criteria = if most then mostCommon !! position else leastCommon !! position