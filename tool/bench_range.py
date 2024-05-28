from timeit import timeit

def tm(stmt, setup):
    t = timeit(stmt='x in range(1, 10)',  setup='x = 5', number=int(2e6))
    print(t, '\t', stmt)

if __name__ == '__main__':
    #   The low end of the range differs by 1 here between the range(l,h)
    #   version and the (l < i < h) version. We ignore this because the
    #   number we're comparing isn't there so it doesn't matter, and adding
    #   the appropriate (l+1) to the benchmark could influence it.
    l = 0; h = 10
    tm(stmt='x in range(l, h)', setup='x = 5')
    tm(stmt='x in r',           setup='x = 5; r = range(l,h)')
    tm(stmt='(l < x < h)',     setup='x = 5')


''' It appears that using ``i in range(l,h)`` vs. ``(l < i < h)`` is much
    of a muchness; they're both pretty much the same speed. I had thought
    that the range one might be faster since it's `entirely in C`_, but
    nope; the "extra" Python parsing for two compare calls seems to make
    no difference.

    .. _entirely in C: https://github.com/python/cpython/blob/5ef5622543844bad1f9bc770ddaaddd2615b8466/Objects/rangeobject.c#L438-L480

0.31942845101002604      x in range(l, h)
0.3192160720936954       x in r
0.31863972696010023      (l < x < h)

0.3301306429784745       x in range(l, h)
0.33534420805517584      x in r
0.3346295360242948       (l < x < h)

0.327112045022659        x in range(l, h)
0.3493508960818872       x in r
0.3452079069102183       (l < x < h)

0.336886431905441        x in range(l, h)
0.33731374703347683      x in r
0.3360138109419495       (l < x < h)

0.32656207599211484      x in range(l, h)
0.3396225399337709       x in r
0.33957852504681796      (l < x < h)

0.3356067721033469       x in range(l, h)
0.35379368090070784      x in r
0.335400736075826        (l < x < h)

0.3356543740956113       x in range(l, h)
0.336340353009291        x in r
0.3366035759681836       (l < x < h)
'''
