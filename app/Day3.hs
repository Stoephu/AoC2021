import Debug.Trace

main :: IO ()
main = do
    contents <- readFile "inputs/small.txt"
    let listOfLine = lines contents
    let gamma = map mostCommonBin $ transposeStrings (map charToString $ head listOfLine) (tail listOfLine)
    let epsilon = negateBin gamma
    print gamma
    print epsilon
    print $  bin2dec (concat gamma) * bin2dec (concat epsilon)
    -- part due
    let temp1 = concat $ search gamma $ map (map charToString) listOfLine :: String
    print $ bin2dec temp1 
    let temp2 = concat $ search epsilon $ map (map charToString) listOfLine :: String
    print $ bin2dec temp2

bin2dec :: [Char] -> Int
bin2dec = foldl (\acc x -> acc*2 + charToInt x) 0

charToString :: Char -> String
charToString =(:[])

charToInt :: Char -> Int
charToInt c = read $ charToString c

transposeStrings = foldl (\acc newString -> [a ++ b| (a,b) <- zip acc $ map charToString newString]) 

mostCommonBin string =  if foldl (\acc x -> if x == '1' then acc + 1 else acc) 0 string > half then "1" else "0"
    where half = div (length string) 2


negateBin [] = []
negateBin ("1":xs) = "0":negateBin xs
negateBin ("0":xs) = "1":negateBin xs




search :: [String] -> [[String]] -> [String]
search (criteria:crits) strings | trace ("Criteria " ++ criteria ++ ":" ++ show crits ++ "strings " ++ show strings) False = search crits $ filter (\x -> criteria == x !! (length x - length crits - 1)) strings