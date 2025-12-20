# This is for sorting the data before it is bulk added 
# I chose quick sort because it has quick in its name, couldn't remeber which of the ones we covered was the best
# x is just records, didn't change it so I didn't have to edit the entire thing from my notes

class QuickSort:
    def __init__(self):
        self.field = None

    def get_value(self, item):
        if self.field == "release_date":
            return item.release_date
        elif self.field == "revenue":
            return item.revenue
        elif self.field == "rating":
            return item.rating
        elif self.field == "min_duration":
            return item.min_duration

    def quickSort(self, x, field, start = 0, end = -1):
        self.field = field
        #print(f"Start: {start}, End: {end}")
        #print(x)
        if len(x) == 0: # handles if there is no list
            return x
        if end == -1: # handles the situation where the list is just one
            end = len(x)-1
        if end-start <= 0: # too small, stop
            return x
        
        #leftEnd, rightStart = naivePartition(x, start, end)
        #leftEnd, rightStart = lomutoPartition(x, start, end)
        leftEnd, rightStart = self.hoarePartition(x, start, end)
        #print(f"leftEnd = {leftEnd}, rightStart = {rightStart}")
        self.quickSort(x, field, start, leftEnd)
        self.quickSort(x, field, rightStart, end)
        return x

    def hoarePartition(self, x, start, end):

        pivot = self.get_value(x[start])
        i = start
        j = end
        while (i < j):
            # move i right until x[i] >= pivot
            while(i < end and self.get_value(x[i]) < pivot):
                i += 1
            # move j left until x[j] < pivot # might need to add =
            while(j > start and self.get_value(x[j]) >= pivot):
                j -= 1
            if j < i:
                break
            # swap the two
            x[i], x[j] = x[j], x[i]
            i += 1
        leftEnd = j
        rightStart = i
        return leftEnd, rightStart