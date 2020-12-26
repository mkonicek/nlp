## What is this repo?

This code lets you experiment with pre-trained word embeddings using plain Python 3 with no additional dependencies.

See the blog post [Playing with word vectors](https://coding-time.co/playing-with-word-vectors) for a detailed explanation.

## Usage

Once you clone this repo, you can simply run:

```
$ python3 main.py
```

Try to edit the code to explore the word embeddings.

This repo only includes a small data file with 1000 words. To get interesting results you'll need to download the [pre-trained word vectors from the fastText website](https://fasttext.cc/docs/en/english-vectors.html).

But don't use the whole 2GB file! The program would use too much memory. Instead, once you download the file take only the top n words, save them to a separate file, and remove the first line. For example:

```
$ cat data/wiki-news-300d-1M.vec | head -n 50001 | tail -n 50000 > data/vectors.vec
```

## Using numpy?

The code doesn't use [numpy](http://www.numpy.org/) or any third party dependencies. This is so that anyone can run the code easily using vanilla Python 3.

There is a [separate branch](https://github.com/mkonicek/nlp/tree/numpy) that uses numpy for the vector math and achieves about 12x speedup on my laptop.

## Type annotations

I'm using the [mypy type checker](http://mypy-lang.org/) to find bugs as I type in Atom (using this [Atom plugin](https://atom.io/packages/linter-mypy)). However, you don't need to have mypy installed. Python 3 will run the code fine.

## LICENSE

MIT
