
# File:     timsort.py
# Author:   John Longley
# Date:     October 2022

# Template file for Inf2-IADS (2022-23) Coursework 1, Part A
# Simplified version of Timsort sorting algorithm


# Provided code for splitting list into suitable segments

# Tags for segment types:

Inc, Dec, Unsorted = +1, -1, 0

# Representing segments (L[start],...,L[end-1]):

class Segment:
    def __init__(self,start,end,tag):
        self.start = start
        self.end = end
        self.tag = tag
    def len(self):
        return self.end - self.start
    def __repr__(self):
        return ('Segment('+str(self.start)+','+str(self.end)+','
                +str(self.tag)+')')

# Stage 1: Split entire list into Inc and Dec segments (possibly very short).

class IncDecRuns:
    def __init__(self,L,key=lambda x:x):
        self.L = L
        self.key = key
        self.m = len(L)-1
        self.dir = Inc if key(L[1]) >= key(L[0]) else Dec
        self.i = 0  # most recent segment boundary
        self.j = 0  # position reached

    def next(self):
        # returns tuple for next segment, or None if end reached
        if self.j == self.m:
            return None
        else:
            self.i = self.j
            # scan for next change of direction
            while (self.j < self.m and
                   ((self.dir == Inc and
                     self.key(self.L[self.j]) <= self.key(self.L[self.j+1])) or
                    (self.dir == Dec and
                     self.key(self.L[self.j]) >= self.key(self.L[self.j+1])))):
                self.j+=1
            if self.j == self.m:
                # no change of direction at final step: include last list entry
                return Segment(self.i, self.m+1, self.dir)
            else:
                # change of direction
                self.dir = -self.dir
                return Segment(self.i, self.j, -self.dir)
    def finished(self):
        return (self.j == self.m)
            
# Stage 2: Fuse consecutive short segments into longer (unsorted) ones.

# Preserve all Inc or Dec runs of at least this size:
runThreshold = 32

class FuseSegments:
    def __init__(self,IncDecRuns):
        self.IDR = IncDecRuns
        self.next1 = self.IDR.next()
        self.next2 = self.IDR.next()

    def next(self):
        if self.next2 == None:
            curr = self.next1
            self.next1 = None
            return curr
        elif self.next1.len() < runThreshold and self.next2.len() < runThreshold:
            # two short segments: fusing required
            start = self.next1.start
            # find end of run of short segments
            while self.next2.len() < runThreshold and not self.IDR.finished():
                self.next2 = self.IDR.next()
            if self.next2.len() < runThreshold:
                # next2 is last segment and is short: include in fused segment
                end = self.next2.end
                self.next1, self.next2 = None, None
            else:
                # next2 is long: exclude from fused segment
                end = self.next2.start
                self.next1 = self.next2
                self.next2 = self.IDR.next()
            return Segment(start, end, Unsorted)
        else:
            # long or isolated short segment: return unchanged
            curr = self.next1
            self.next1 = self.next2
            self.next2 = self.IDR.next()
            return curr
    def finished(self):
        return (self.next1 == None)

# Stage 3: Split long unsorted segments into ones of length in range
# blockMin,...,blockMax (suitable for InsertSort).
# Return a list of all segments.

blockMin = 32
blockMax = 63  # require blockMax >= blockMin*2+1

def segments(L, key=lambda x:x):
    FS = FuseSegments(IncDecRuns(L, key))
    S = []
    curr = FS.next()
    while curr != None:
        if curr.len() == 1 and len(S) >= 1 and not FS.finished():
            # drop this segment, just tag extra element onto previous one
            S[-1].end += 1
        elif curr.tag != Unsorted or curr.len() <= blockMax:
            # keep segment as is
            S.append(curr)
        else:
            # split long unsorted segment into blocks
            start = curr.start
            n = curr.len()
            k = n // blockMin
            divs = [start+(n*i)//k for i in range(k+1)]
            for i in range(k):
                S.append(Segment(divs[i], divs[i+1], 0))
        curr = FS.next()
    return S


# TODO: Task 1.
#   insertSort(L,start,end,key=lambda x:x)
#   reverse(L, start, end)
#   processSegments(L, segs, key=lambda x: x):

# in-place InsertSort to sort the portion of L from L[start] to L[end-1] inclusive
def insertSort(L, start, end, key=lambda x: x):
    for i in range(start + 1, end):
        x = L[i]
        j = i - 1
        while j >= start and key(L[j]) >= key(x):
            L[j + 1] = L[j]
            j = j - 1
        L[j + 1] = x


# reverse the portion of L from L[start] to L[end-1] inclusive
def reverse(L, start, end):
    for i in range((end - start)//2):
        # swap the values of L[start + i] and L[end - 1 - i].
        x = L[start + i]
        L[start + i] = L[end - 1 - i]
        L[end - 1 - i] = x


# takes a list L and a list segs of Segment objects (of the kind returned by segments),
# and applies the appropriate processing to each segment in turn
def processSegments(L, segs, key=lambda x: x):
    for seg in segs:
        if seg.tag == Unsorted:
            insertSort(L, seg.start, seg.end, key)
        elif seg.tag == Dec:
            reverse(L, seg.start, seg.end)


# TODO: Task 2.
#   mergeSegments(L,seg1,seg2,M,start,key=lambda x:x)
#   copySegment(L,seg,M,start)


# take a list L and two Segment objects, and writes the merged (sorted) segment into M beginning at position start
def mergeSegments(L, seg1, seg2, M, start, key=lambda x:x):
    i = seg1.start
    j = seg2.start
    length = seg1.len() + seg2.len()

    for k in range(length):
        # if all elements in one list are all copied in the M.
        if i == seg1.end:
            M[start + k] = L[j]
            j = j + 1
        elif j == seg2.end:
            M[start + k] = L[i]
            i = i + 1

        elif key(L[i]) < key(L[j]):
            M[start + k] = L[i]
            i = i + 1
        elif key(L[i]) >= key(L[j]):
            M[start + k] = L[j]
            j = j + 1

    return length


# copy a given segment of L into M, beginning at position start.
def copySegment(L, seg, M, start):
    for i in range(seg.len()):
        M[start + i] = L[seg.start + i]

    return seg.len()


# TODO: Task 3.
#   mergeRound(L, segs, M,key=lambda x:x)
#   mergeRounds(L, segs, M,key=lambda x:x):

# merge the segments in pairs, and fill up M from left to right with the results of the merges.
def mergeRound(L, segs, M, key=lambda x:x):
    newSegs = []
    for i in range(len(segs)//2):
        start = (segs[2 * i]).start
        length = mergeSegments(L, segs[2 * i], segs[2 * i + 1], M, start, key)
        newSegs.append(Segment(start, start + length, 1))

    # if there is one segment left, the last segment should simply be copied
    # into the rightmost portion of M so that M is completely filled up.
    if len(segs) % 2 == 1:
        start = (segs[-1]).start
        length = copySegment(L, segs[-1], M, start)
        newSegs.append(Segment(start, start + length, 1))
    return newSegs


def mergeRounds(L, segs, M, key=lambda x:x):
    # the indicator: after the mergeRound, L is one step ahead.
    rightPlace = True

    while len(segs) != 1:
        if rightPlace:
            segs = mergeRound(L, segs, M, key)
            rightPlace = False
        elif not rightPlace:
            segs = mergeRound(M, segs, L, key)
            rightPlace = True

    # if L is not the sorted list, simply let L = M.
    if not rightPlace:
        L = M
    return L


# Provided code:

def SimpleTimSort(L, key=lambda x:x):
    if len(L) <= 1:
        return L
    else:
        segs = segments(L, key)
        processSegments(L, segs, key)
        M = [None] * len(L)
        return mergeRounds(L, segs, M, key)

# End of file
