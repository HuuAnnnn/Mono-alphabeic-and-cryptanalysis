# Mono-alphabetic and frequency analysis to break this code
I use the n-grams method to break the cipher which is decrypted by mono-alphabetic

How to run the test?
Use this command below, `n` is n-grams (X={1, 2, 3, 4, 5}), `l` is the length of sample (X={50, 100, 500, 1000, 5000})
```
    make n=? l=?
```
Example:
```
    make n=5 l=100
```
That means, We will decrypt cipher text using `quintgrams` and use a sample `100 words`