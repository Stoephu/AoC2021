import System.IO


main :: IO ()
main = do
    handle <- openFile "inputs/test.txt" ReadMode
    contents <- hGetContents handle
    putStr contents
    hClose handle