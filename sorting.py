assert __name__ == "__main__", "importing doesn't work yet, sorry!"

TO_DO = """TO-DO LIST:
* Update the GUI using .grid or tk.Frame
* Add time/space complexities for sorts
* Add labels for sort stats
* Add a "real time" label
* Add a button to set the recursion limit
* Add a way to specify sort parameters (ex. base)
* Implement an aux-(array/structure) system   [done?]
* Implement a color system
* Finish/fix sorts"""

print(TO_DO)

BG = "#eee"
ICON = "Put icon data here, or a file name."
ICON_FROMFILE = False
HIDE_PYGAME = True
LOAD_ICON = False
MIN_FREQ = 19
MAX_FREQ = 590
VOLUME = 0.15

import tkinter as tk

from tkinter.messagebox import askyesno, showerror, showinfo
from tkinter.filedialog import askopenfilename

import sys
import os

from asyncio import run as aio_run, gather as aio_gather, sleep as aio_sleep
from random import randrange, shuffle, seed
from math import sqrt, floor, ceil, log
from time import sleep, perf_counter
from traceback import format_exc
from io import BytesIO, StringIO

sys.setrecursionlimit(2147483617)

root = tk.Tk()
root.title("Initializing...")
root.config(bg=BG)
root.geometry("1100x600")
root.resizable(False, False)

class CancelSort(KeyboardInterrupt):
    "The sort was cancelled by the user."

class Array(list):
    "The class used to visualize arrays."
    def __init__(self, lst):
        super().__init__(lst)
        self.length = super().__len__()
        self.comps = 0
        self.swaps = 0
        self.writes = 0
        self.reversals = 0
        self.frames = 0
        self.passed = 0
        self.sounds = []
        self.max_item = max(self)
        self.aux_writes = 0
        self.draw_stats = [{"value": None, "color": None, "id": None}
                           for i in range(len(self))] + [self.max_item]
        self.first = True
    def stat_check(func):
        "Returns a decorator that raises CancelSort if 'running' is False."
        def decorator(*args, **kwargs):
            try:
                global running
                if not running:
                    raise CancelSort
                return func(*args, **kwargs)
            except:
                args[0].clear_sounds()
                raise
        decorator.__doc__ = func.__doc__
        return decorator
    def bad_type(msg):
        "Returns a decorator that raises TypeError."
        def decorator(*args, **kwargs):
            "Bad type."
            raise TypeError(msg)
        return decorator
    __delitem__ = bad_type("cannot delete item from Array")
    __iadd__ = bad_type("cannot add to Array")
    __imul__ = bad_type("cannot multiply Array")
    append = bad_type("cannot append to Array")
    pop = bad_type("cannot pop from Array")
    clear = bad_type("cannot clear Array")
    extend = bad_type("cannot extend Array")
    insert = bad_type("cannot insert to Array")
    remove = bad_type("cannot remove from Array")
    sort = bad_type("No.")
    @stat_check
    def __len__(self):
        return self.length
    @stat_check
    def __getitem__(self, index):
        return super().__getitem__(index)
    @stat_check
    def __setitem__(self, index, value):
        super().__setitem__(index, value)
    # No stat check for sounds
    def clear_sounds(self):
        "Stop all sounds playing."
        for i in self.sounds:
            i.stop()
        self.sounds.clear()
    @stat_check
    def refresh(self, *colored, analyze=False, done=False):
        "Refresh the canvas."
        self.clear_sounds()
        if self.first:
            canvas.delete("all")
            self.first = False
        if self.passed >= self.frames:
            self.passed = -1
            max_change = self.max_item != self.draw_stats[len(self)]
            if max_change:
                self.draw_stats[len(self)] = self.max_item
            for i in range(len(self)):
                stats = self.draw_stats[i]
                if done and i <= colored[0]:
                    color = "#0e0"   # green
                elif i in colored:
                    if sound_var.get():
                        sound = Sound(square(sin(2 * pi * arange(44100) * (self[
                            i] / self.max_item * ((MAX_FREQ * 4) - (MIN_FREQ * 4
                            )) + (MIN_FREQ * 4)) / 44100)).astype(float32))
                        sound.set_volume(VOLUME)
                        sound.play()
                        self.sounds.append(sound)
                    if color_var.get():
                        color = "black"
                    else:
                        color = "blue" if analyze else "red"
                else:
                    if color_var.get():
                        raise CancelSort("color hasn't been implemented yet")
                    else:
                        color = "black"
                rect_id = stats["id"]
                if stats["value"] != self[i] or max_change:
                    canvas.delete(rect_id)
                    self.draw_stats[i] = {"color": color, "value": self[i],
                        "id": canvas.create_rectangle(i * (800 / len(self)),
                        -((600 * (self[i] / self.max_item)) - 600), (i + 1)
                        * (800 / len(self)), 600, outline=color, fill=color)}
                elif stats["color"] != color:
                    canvas.itemconfig(rect_id, outline=color, fill=color)
                    self.draw_stats[i]["color"] = color
            canvas.update()
        self.passed += 1
    @stat_check
    def compare(self, i1, i2, refresh=True):
        "Returns 1 if i1 > i2, -1 if i1 < i2, and 0 if i1 == i2."
        self.comps += 1
        comps.config(text="Comparisons: %s" % self.comps)
        if refresh:
            self.refresh(i1, i2)
        return 1 if self[i1] > self[i2] else -1 if self[i1] < self[i2] else 0
    @stat_check
    def swap(self, i1, i2, refresh=True):
        "Swaps the two indexes."
        self.writes += 2
        self.swaps += 1
        writes.config(text="Writes: %s" % self.writes)
        swaps.config(text="Swaps: %s" % self.swaps)
        self[i1], self[i2] = self[i2], self[i1]
        if refresh:
            self.refresh(i1, i2)
    @stat_check
    def write(self, i, n, update_max=False, refresh=True):
        "Writes value n to index i."
        self.writes += 1
        writes.config(text="Writes: %s" % self.writes)
        self[i] = n
        if update_max:
            self.max_item = max(self)
        if refresh:
            self.refresh(i)
    @stat_check
    def get_max(self, start=0, stop=None):
        "Return the maximum index within start and stop."
        if stop is None:
            stop = len(self)
        new = start
        start += 1
        while start < stop:
            self.comps += 1
            comps.config(text="Comparisons: %s" % self.comps)
            self.refresh(new, start, analyze=True)
            if self[start] > self[new]:
                new = start
            start += 1
        return new
    @stat_check
    def get_min(self, start=0, stop=None):
        "Return the minimum index within start and stop."
        if stop is None:
            stop = len(self)
        new = start
        start += 1
        while start < stop:
            self.comps += 1
            comps.config(text="Comparisons: %s" % self.comps)
            self.refresh(new, start, analyze=True)
            if self[start] < self[new]:
                new = start
            start += 1
        return new
    @stat_check
    def reverse(self, start=None, stop=None):
        "Reverse the array."
        if start is None:
            if stop is None:
                start, stop = 0, len(self)
            else:
                start, stop = 0, start
        stop -= 1
        self.reversals += 1
        reversals.config(text="Reversals: %s" % self.reversals)
        for i in range((stop - start + 1) // 2):
            self.swap(start, stop)
            start += 1
            stop -= 1
    @stat_check
    def compare_values(self, i, v, refresh=True):
        "Compares values i and v."
        self.comps += 1
        comps.config(text="Comparisons: %s" % self.comps)
        if refresh:
            self.refresh(i)
        return 1 if i > v else -1 if i < v else 0
    @stat_check
    def get(self, i):
        "Return self[i]."
        self.refresh(i, analyze=True)
        return self[i]
    @stat_check
    def write_aux(self, aux, index, val):
        "Write to an aux array."
        self.aux_writes += 1
        aux_writes.config(text="Aux writes: %s" % self.aux_writes)
        aux[index] = val
    @stat_check
    def swap_aux(self, aux, i1, i2):
        "Swap to an aux array."
        self.aux_writes += 2
        aux_writes.config(text="Aux writes: %s" % self.aux_writes)
        aux[i1], aux[i2] = aux[i2], aux[i1]
    @stat_check
    def append_aux(self, aux, val):
        "Append to an aux array."
        self.aux_writes += 1
        aux_writes.config(text="Aux writes: %s" % self.aux_writes)
        aux.append(val)
    @stat_check
    def step(self, lo, hi):
        "Compare (and swap if nexessary) indexes lo and hi."
        if self.compare(lo, hi) == 1:
            self.swap(lo, hi)
    @stat_check
    def incr_comps(self):
        "Increment the comparisons."
        self.comps += 1
        comps.config(text="Comparisons: %s" % self.comps)
Array.stat_check = staticmethod(Array.stat_check)
Array.bad_type = staticmethod(Array.bad_type)

sort_dict = {}
def Sort(name=None, sort_type="<NULL>", limit=None, stable="<NULL>",
         best_time="<NULL>", average_time="<NULL>", worst_time="<NULL>",
         best_space="<NULL>", average_space="<NULL>", worst_space="<NULL>",
         option_dict={}, *, unfinished=False, disabled=False):
    "A decorator that adds the function to the list of sorts."
    class Decorator:
        def __init__(self, name, sort_type, limit, stable, best_time,
                     average_time, worst_time, best_space, average_space,
                     worst_space, unfinished, *options):
            self.name = name
            self.sort_type = sort_type
            if type(limit) != int and limit is not None:
                raise TypeError("limit must be int or None")
            self.limit = limit
            self.stable = stable
            self.time = (best_time, average_time, worst_time)
            self.space = (best_space, average_space, worst_space)
            self.option_dict = option_dict
            self.unfinished = unfinished
            self.disabled = disabled
        def __call__(self, func):
            global sorts, dropdown
            if self.name is None:
                self.name = func.__name__
            if not self.disabled:
                sorts.append(self.name)
                sorts = sorted(sorts)
                dropdown.destroy()
                dropdown = tk.OptionMenu(root, selected, *sorts, command=add_sort)
                dropdown.config(bg=BG)
                dropdown.pack()
                sort_dict[self.name] = func
            return func
    return Decorator(name, sort_type, limit, stable, best_time, average_time,
                     worst_time, best_space, average_space, worst_space,
                     option_dict, unfinished, disabled)

shuffle_dict = {}
shuffles = []
def Shuffle(name=None, *, unfinished=False, disabled=False):
    "A decorator that adds the function to the list of shuffles."
    class Decorator:
        def __init__(self, name, unfinished, disabled):
            self.name = name
            self.unfinished = unfinished
            self.disabled = disabled
        def __call__(self, func):
            global shuffles, s_dropdown
            if self.name is None:
                self.name = func.__name__
            if not self.disabled:
                shuffle_dict[self.name] = func
                shuffles.append(self.name)
                shuffles = sorted(shuffles)
                s_dropdown.destroy()
                s_dropdown = tk.OptionMenu(root, shuffle_selected, *shuffles,
                                           command=add_shuffle)
                s_dropdown.config(bg=BG)
                s_dropdown.pack()
            return func
    return Decorator(name, unfinished, disabled)

sorts = []

shuffle_bool = False
def add_shuffle(option):
    global shuffle_bool
    shuffle_bool = True
    enable_run()

sort_bool = False
def add_sort(option):
    global sort_bool
    sort_bool = True
    enable_run()

def enable_run():
    global shuffle_bool, sort_bool, run
    if shuffle_bool and sort_bool:
        run.config(state="normal")

canvas = tk.Canvas(root, width=800, height=600, bg=BG, highlightthickness=0)
canvas.pack(side="left")

selected = tk.StringVar(root, "Choose Sort")
dropdown = tk.OptionMenu(root, selected, None)
dropdown.config(bg=BG, state="disabled")
dropdown.pack()

def reset_stats(arr=None):
    swaps.config(text="Swaps: 0")
    comps.config(text="Comparisons: 0")
    writes.config(text="Writes: 0")
    reversals.config(text="Reversals: 0")
    real_time.config(text="Real time: Unfinished")
    aux_writes.config(text="Aux writes: 0")
    if arr:
        arr.comps = 0
        arr.swaps = 0
        arr.writes = 0
        arr.reversals = 0
        arr.aux_writes = 0

def run_sort():
    global sort_dict, shuffle_dict, running
    if not textbox.get():
        showerror("Invalid Length", "The length cannot be empty!")
        return
    length = int(textbox.get())
    if length < 2:
        showerror("Too Small", "The length of the array must be at least two!")
        return
    if length >= 256:
        if askyesno("Large Array", "This visualizer is not meant for large \
array sizes. Even with lots of dropped frames, it will likely take a while for \
it to finish.\nContinue?") == False:
            return
    if not dropped.get():
        showerror("Invalid Frames", "The amount of frames dropped cannot be empty!")
        return
    running = True
    arr = Array(list(range(1, length + 1)))
    arr.frames = orig_frames = float(dropped.get())
    reset_stats(arr)
    try:
        shuffle_dict[shuffle_selected.get()](arr)
    except BaseException as err:
        if type(err) == KeyboardInterrupt:
            sys.stderr.write(format_exc())
            raise SystemExit
        if type(err) != CancelSort:
            sys.stderr.write("Traceback in shuffle algorithm %s:\n%s"
                             % (selected.get(), format_exc()[35:]))
            showerror("Error in Shuffle",
                      "The shuffle failed because of an error: %s"
                      % format_exc())
        return
    running = True
    arr.frames = 0
    arr.refresh()
    arr.frames = orig_frames
    sleep(1)
    reset_stats(arr)
    try:
        sort_dict[selected.get()](arr)
    except BaseException as err:
        if type(err) == KeyboardInterrupt:
            sys.stderr.write(format_exc())
            raise SystemExit
        if type(err) != CancelSort:
            sys.stderr.write("Traceback in sorting algorithm %s:\n%s"
                             % (selected.get(), format_exc()[35:]))
            showerror("Error in Sort", "The sort failed because of an error: %s"
                      % format_exc())
        return
    arr.frames = 0
    arr.refresh()
    arr.frames = floor(sqrt(len(arr))) // 3
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            showerror("Sort Failed", "The sort failed to create a sorted version \
of the array; indicies %s and %s are out of order!" % (i, i + 1))
            arr.refresh()
            return
        arr.refresh(i, done=True)
    arr.frames = 0
    arr.refresh(len(arr) - 1, done=True)
    sleep(0.1)
    arr.refresh()

run = tk.Button(text="Run Sort", state="disabled", highlightbackground=BG,
                command=run_sort)
run.pack()

def validate_positive(var):
    try:
        return int(var) > 0
    except ValueError:
        return not var
length = tk.StringVar(root)
length.set(32)
textbox = tk.Entry(root, width=5, textvariable=length, highlightbackground=BG,
                   justify="right", validate="key", vcmd=(root.register(
                       validate_positive), "%P"))
textbox.pack()

def validate_nonnegative(var):
    try:
        return float(var) >= 0
    except ValueError:
        return not var
dropped = tk.StringVar(root)
dropped.set(0)
dropped_text = tk.Entry(root, width=5, textvariable=dropped, justify="right",
                        highlightbackground=BG, validate="key", vcmd=(
                            root.register(validate_nonnegative), "%P"))
dropped_text.pack()

def ext_import():
    file = askopenfilename(filetypes=(("Python Scripts", "*.py"),
                                      ("Python Scripts", "*.pyw")))
    if file:
        with open(file) as f:
            exec(f.read())

sort_import = tk.Button(root, text="Import Script", command=ext_import,
                        highlightbackground=BG)
sort_import.pack()

shuffle_selected = tk.StringVar(root, "Choose Shuffle")
s_dropdown = tk.OptionMenu(root, shuffle_selected, None)
s_dropdown.config(state="disabled", bg=BG)
s_dropdown.pack()

swaps = tk.Label(root, text="Swaps: 0", bg=BG)
swaps.pack()
comps = tk.Label(root, text="Comparisons: 0", bg=BG)
comps.pack()
writes = tk.Label(root, text="Writes: 0", bg=BG)
writes.pack()
reversals = tk.Label(root, text="Reversals: 0", bg=BG)
reversals.pack()
aux_writes = tk.Label(root, text="Aux writes: 0", bg=BG)
aux_writes.pack()
real_time = tk.Label(root, text="Real time: Unfinished", bg=BG)
real_time.pack()

def set_running():
    global running
    running = False
stop = tk.Button(root, text="Cancel Sort", command=set_running,
                 highlightbackground=BG)
stop.pack()

color_var = tk.BooleanVar(root)
use_color = tk.Checkbutton(root, text="Use Color", variable=color_var, bg=BG)
use_color.config(state="disabled")
use_color.pack()

sound_var = tk.BooleanVar(root)
use_sound = tk.Checkbutton(root, text="Use Sound", variable=sound_var, bg=BG)
use_sound.config(state="disabled")
use_sound.pack()

running = True
arr = list(range(1, 33))
shuffle(arr)
arr = Array(arr)
arr.max_item = 32
arr.refresh()
running = False

# ------------------------ Built-in sorts and shuffles -------------------------

@Shuffle("Random Unique")
def RandomUnique(arr):
    for i in range(1, len(arr)):
        arr.swap(i, randrange(i + 1))

@Shuffle("Already Sorted")
def AlreadySorted(arr):
    pass

@Shuffle("Random Few Unique")
def RandomFewUnique(arr):
    lst = list(range(1, floor(sqrt(len(arr))) + 1))
    while len(lst) < len(arr):
        lst *= 2
    while len(lst) > len(arr):
        del lst[-1]
    for index, i in enumerate(lst):
        arr.write(index, i, True)
    RandomUnique(arr)

@Shuffle("Reversed Few Unique")
def ReversedFewUnique(arr):
    lst = list(range(1, floor(sqrt(len(arr))) + 1))
    while len(lst) < len(arr):
        lst *= 2
    while len(lst) > len(arr):
        del lst[-1]
    for index, i in enumerate(sorted(lst)):
        arr.write(index, i, True)
    arr.reverse()

@Shuffle("Reversed")
def Reversed(arr):
    arr.reverse()

@Shuffle("Recursive Reversed")
def RecursiveReversed(arr):
    def wrapper(start, stop):
        arr.reverse(start, stop)
        if stop - start > 2:
            wrapper(start, (stop - start) // 2 + start)
            wrapper((stop - start) // 2 + start, stop)
    wrapper(0, len(arr))

@Shuffle("Stooge Recursive Reversed")
def StoogeRecursiveReversed(arr):
    def wrapper(start, stop):
        arr.reverse(start, stop)
        if stop - start + 1 > 2:
            wrapper(start, ceil(stop - ((stop - start + 1) / 3)))
            wrapper(floor(start + ((stop - start + 1) / 3)), stop)
            wrapper(start, ceil(stop - ((stop - start + 1) / 3)))
    wrapper(0, len(arr))

@Shuffle("Reversed Primes")
def ReversedPrimes(arr):
    primes = []
    n = 2
    while len(primes) < len(arr):
        flag = False
        for i in range(2, n // 2 + 1):
            if not n % i:
                flag = True
        if not flag:
            primes.append(n)
        n += 1
    arr.max_item = primes[-1]
    for index, i in enumerate(primes):
        arr.write(index, i)
    arr.reverse()

@Shuffle("Fly Straight Dangit")
def FlyStraightDangit(arr):
    def sequence(n):
        def gcd(a, b):
            for i in range(min(a, b), 1, -1):
                if not (a % i or b % i):
                    return i
        if n in [0, 1]:
            return 1
        n_minus1 = sequence(n - 1)
        n_gcd = gcd(n_minus1, n)
        if n_gcd:
            return int(n_minus1 / n_gcd)
        return n_minus1 + n + 1
    lst = []
    for i in range(len(arr)):
        new = sequence(arr[i])
        arr.write(i, new, update_max=True)
        lst.append(new)

@Shuffle("Leonardo Numbers")
def LeonardoNumbers(arr):
    lst = [1, 1]
    def sequence(n):
        if n in [0, 1]:
            return 1
        result = lst[n - 1] + lst[n - 2] + 1
        lst.append(result)
        return result
    for index, i in enumerate(arr):
        arr.write(index, sequence(i), update_max=True)
    arr.reverse()

@Shuffle("Predictable Random Unique")
def PredictableRandomUnique(arr):
    seed(0)
    RandomUnique(arr)
    seed(perf_counter())

@Shuffle("No Unique")
def NoUnique(arr):
    arr.max_item = 2
    for i in range(len(arr)):
        arr.write(i, 1)

@Shuffle("Max Heapified")
def MaxHeapified(arr):
    def sift_down(node):
        left = node * 2 + 1
        if left < len(arr):
            right = left + 1
            if right < len(arr) and arr.compare(left, right) == -1:
                index = right
            else:
                index = left
            if arr.compare(node, index) == -1:
                arr.swap(node, index)
                sift_down(index)
    for node in range(len(arr) - 1, -1, -1):
        sift_down(node)

@Shuffle("Bit Reversed")
def BitReversed(arr):
    minimum = min(arr)
    length = len(bin(max(arr) - minimum)) - 2
    for i in range(len(arr)):
        binary = bin(arr[i] - minimum)[2:]
        while len(binary) < length:
            binary = "0" + binary
        arr.write(i, eval("0b" + binary[::-1]) + minimum, update_max=True)

def MinHeapified(arr, reverse=False):
    if reverse:
        arr.reverse()
    def sift_down(node):
        left = node * 2 + 1
        if left < len(arr):
            right = left + 1
            if right < len(arr) and arr.compare(left, right) == 1:
                index = right
            else:
                index = left
            if arr.compare(node, index) == 1:
                arr.swap(node, index)
                sift_down(index)
    for node in range(len(arr) - 1, -1, -1):
        sift_down(node)

@Shuffle("Min Heapified")
def MinHeapifiedShuffle(arr):
    MinHeapified(arr, reverse=True)

@Shuffle("Modulo Shuffle")
def ModuloShuffle(arr):
    for i in range(1, len(arr) + 1):
        arr.write(i - 1, len(arr) % i + 1, update_max=True)

@Shuffle("Half Reversed")
def HalfReversed(arr):
    i, j = 0, len(arr) - 1
    while i < j:
        arr.write(j, arr[i], update_max=True)
        j -= 1
        i += 1

@Shuffle("Factors")
def Factors(arr):
    for i in range(len(arr), 0, -1):
        factors = 1 + (i > 1)
        for j in range(2, i // 2 + 1):
            if not i % j:
                factors += 1
        arr.write(i - 1, factors, update_max=True)

@Shuffle("Almost Sorted")
def AlmostSorted(arr):
    for i in range(ceil(sqrt(len(arr)))):
        arr.swap(randrange(len(arr)), randrange(len(arr)))

@Sort("Bubble Sort", "Comparison", 2048, True, "n^2", "n^2", "n^2", 1, 1, 1)
def BubbleSort(arr):
    for i in range(len(arr) - 1):
        for j in range(len(arr) - 1):
            if arr.compare(j, j + 1) == 1:
                arr.swap(j, j + 1)

@Sort("Insertion Sort", "Comparison", 2048, True, "n", "n^2", "n^2")
def InsertionSort(arr):
    for i in range(len(arr) - 1):
        while arr.compare(i, i + 1) == 1 and i > -1:
            arr.swap(i, i + 1)
            i -= 1

@Sort("Optimized Bubble Sort", "Comparison", 2048, True, "n", "n^2", "n^2")
def OptimizedBubbleSort(arr):
    i = 1
    while i < len(arr):
        swapped = False
        streak = 0
        for j in range(len(arr) - i):
            if arr.compare(j, j + 1) == 1:
                arr.swap(j, j + 1)
                swapped = True
                streak = -1
            streak += 1
        if not swapped:
            break
        i += streak + 1

@Sort("Time + Insertion Sort", "Distribution", 1024, False, "max(n)", "max(n)",
      "max(n)", "n", "n", "n")
def TimeInsertionSort(arr, mult=0.00035):
    index = 0
    async def write_to_arr(n):
        nonlocal index
        await aio_sleep(n * mult)
        arr.write(index, n)
        index += 1
    async def main():
        await aio_gather(*[write_to_arr(arr.get(i)) for i in range(len(arr))])
    aio_run(main())
    InsertionSort(arr)

@Sort("Comb Sort")
def CombSort(arr):
    for i in range(len(arr) - 1, 0, -1):
        j = 0
        while i < len(arr):
            if arr.compare(j, i) == 1:
                arr.swap(i, j)
            j += 1
            i += 1

@Sort("Stooge Sort", "Comparison", 32, "n^(log3/log1.5)", "n^(log3/log1.5)",
      "n^(log3/log1.5)", 1, 1, 1)
def StoogeSort(arr):
    def wrapper(start, stop):
        if arr.compare(start, stop) == 1:
            arr.swap(start, stop)
        if stop - start + 1 > 2:
            wrapper(start, ceil(stop - ((stop - start + 1) / 3)))
            wrapper(floor(start + ((stop - start + 1) / 3)), stop)
            wrapper(start, ceil(stop - ((stop - start + 1) / 3)))
    wrapper(0, len(arr) - 1)

@Sort("Hyper Stooge Sort", "Comparison", 16, "3^n", "3^n", "3^n", 1, 1, 1)
def HyperStoogeSort(arr):
    def wrapper(start, stop):
        if arr.compare(start, stop) == 1:
            arr.swap(start, stop)
        if stop - start + 1 > 2:
            wrapper(start, stop - 1)
            wrapper(start + 1, stop)
            wrapper(start, stop - 1)
    wrapper(0, len(arr) - 1)

@Sort("Bogo Sort", "Comparison", 8, "n", "n*n!", "∞", 1, 1, 1)
def BogoSort(arr):
    while True:
        is_sorted = True
        for i in range(len(arr) - 1):
            if arr.compare(i, i + 1) == 1:
                is_sorted = False
                break
        if is_sorted:
            break
        for i in range(1, len(arr)):
            arr.swap(i, randrange(0, i + 1))

@Sort("Selection Sort", "Comparison", 2048, "n^2", "n^2", "n^2", 1, 1, 1)
def SelectionSort(arr):
    for i in range(len(arr) - 1):
        minimum = arr.get_min(i)
        if minimum != i:
            arr.swap(i, minimum)

@Sort("Cocktail Shaker Sort", "Comparison", 2048, "n^2", "n^2", "n^2", 1, 1, 1)
def CocktailShakerSort(arr):
    for i in range(len(arr) // 2):
        for j in list(range(len(arr) - 1)) + list(range(len(arr) - 3, 0, -1)):
            if arr.compare(j, j + 1) == 1:
                arr.swap(j, j + 1)

@Sort("Snuffle Sort", "Comparison", 16, "e^n", "e^n", "e^n", 1, 1, 1)
def SnuffleSort(arr):
    def wrapper(start, stop):
        if arr.compare(start, stop) == 1:
            arr.swap(start, stop)
        if stop - start + 1 > 2:
            new = (stop - start) // 2 + start
            for i in range(ceil((stop - start + 1) / 2)):
                wrapper(start, new)
                wrapper(new, stop)
    wrapper(0, len(arr) - 1)

@Sort("Circle Sort", "Comparison", 2048)
def CircleSort(arr):
    def wrapper(start, stop):
        if stop - start >= 2:
            i, j = start, stop - 1
            while i < j:
                if arr.compare(i, j) == 1:
                    nonlocal swapped
                    swapped = True
                    arr.swap(i, j)
                i += 1
                j -= 1
            wrapper(start, (stop - start) // 2 + start)
            wrapper((stop - start) // 2 + start, stop)
    swapped = True
    while swapped:
        swapped = False
        wrapper(0, len(arr))

@Sort("Bozo Sort", "Comparison", 6)
def BozoSort(arr):
    while True:
        flag = False
        for i in range(len(arr) - 1):
            if arr.compare(i, i + 1) == 1:
                flag = True
                break
        if not flag:
            break
        arr.swap(randrange(len(arr)), randrange(len(arr)))

@Sort("Stable Stooge Sort")
def StableStoogeSort(arr):
    def wrapper(start, stop):
        if stop - start == 1:
            if arr.compare(start, stop) == 1:
                arr.swap(start, stop)
        elif stop - start > 1:
            wrapper(start, ceil(stop - ((stop - start + 1) / 3)))
            wrapper(floor(start + ((stop - start + 1) / 3)), stop)
            wrapper(start, ceil(stop - ((stop - start + 1) / 3)))
    wrapper(0, len(arr) - 1)

@Sort("Odd Even Sort")
def OddEvenSort(arr, base=2):
    for i in range(ceil(len(arr) * ((base - 1) / base))):
        for j in range(base):
            for k in range(j, len(arr) - 1, base):
                if arr.compare(k, k + 1) == 1:
                    arr.swap(k, k + 1)

@Sort("Bidirectional Bubble Sort")
def BidirectionalBubbleSort(arr):
    i = 0
    total = 0
    direction = True
    while total < len(arr):
        plus1 = i + (1 if i < len(arr) - 1 else -i)
        if arr.compare(i, plus1) == (1 if plus1 else -1):
            arr.swap(i, plus1)
            if not direction:
                total = -1
                direction = True
            i += 1 if i < len(arr) - 1 else -i
        else:
            if direction:
                total = -1
                direction = False
            i -= 1 if i else -(len(arr) - 1)
        total += 1

@Sort("Less Bogo Sort")
def LessBogoSort(arr):
    for i in range(len(arr) - 1):
        while not all(arr.compare(i, j) != 1 for j in range(i + 1, len(arr))):
            for j in range(i, len(arr) - 1):
                arr.swap(j, randrange(j, len(arr)))

@Sort("In-Place Merge Sort")
def InPlaceMergeSort(arr):
    def wrapper(start, stop):
        if stop - start > 2:
            wrapper(start, (stop - start) // 2 + start)
            wrapper((stop - start) // 2 + start, stop)
        if stop - start > 1:
            bounds = [start, (stop - start) // 2 + start]
            while bounds[0] < bounds[1] < stop:
                if arr.compare(bounds[0], bounds[1]) == 1:
                    for i in range(bounds[1] - 1, bounds[0] - 1, -1):
                        arr.swap(i, i + 1)
                    bounds[1] += 1
                bounds[0] += 1
    wrapper(0, len(arr))

@Sort("Binary Sort", "Comparison", 12, "2^n", "2^n", "2^n", 1, 1, 1)
def BinarySort(arr):
    current = 1
    while len(bin(current)[2:]) < len(arr):
        new = bin(current)[2:][::-1]
        pos = 0
        while new[pos] != "1":
            pos += 1
        if arr.compare(pos, pos + 1) == 1:
            arr.swap(pos, pos + 1)
        current += 1

@Sort("Selection Bubble Sort")
def SelectionBubbleSort(arr):
    for i in range(len(arr) - 1):
        orig_i = i
        while True:
            i = orig_i
            swap = False
            for j in range(i + 1, len(arr)):
                if arr.compare(i, j) == 1:
                    arr.swap(i, j)
                    swap = True
                    i = j
            if not swap:
                break

@Sort("Gravity Sort", "Distributive", 128, "n^2", "n^2", "n^2", "n*max",
      "n*max", "n*max")
def GravitySort(arr):
    lst = []
    for i in range(len(arr)):
        current = arr.get(i)
        if type(current) != int or current < 0:
            showerror("Cannot Complete", "All values must be non-negative \
integers.")
            raise CancelSort
        lst.append(current)
    lst = [[j >= i for j in lst] for i in range(max(lst), 0, -1)]
    new = []
    for i in range(len(lst[0])):
        current = []
        for j in range(len(lst) - 1, -1, -1):
            current.append(lst[j][i])
        new.append(current)
    lst = new.copy()
    done_index = 0
    while True:
        done = True
        for i in range(len(lst) - 2, done_index - 1, -1):
            for j in range(len(lst[i])):
                if lst[i][j] and not lst[i + 1][j]:
                    lst[i][j], lst[i + 1][j] = lst[i + 1][j], lst[i][j]
                    done = False
        if done:
            break
        for i in range(done_index, len(lst)):
            arr.write(i, sum(lst[i]))
        done_index += 1

@Sort("Shell Sort")
def ShellSort(arr):
    gap = len(arr) // 2
    while gap:
        for i in range(0, len(arr) - gap):
            while arr.compare(i, i + gap) == 1 and i >= 0:
                arr.swap(i, i + gap)
                i -= gap
        gap //= 2

@Sort("Merge Sort")
def MergeSort(arr):
    def wrapper(start, stop):
        if stop - start > 2:
            wrapper(start, (stop - start) // 2 + start)
            wrapper((stop - start) // 2 + start, stop)
        bounds = [start, (stop - start) // 2 + start]
        orig_right = bounds[1]
        new = []
        while bounds[0] < orig_right and bounds[1] < stop:
            if arr.compare(bounds[0], bounds[1]) == 1:
                new.append(arr[bounds[1]])
                bounds[1] += 1
            else:
                new.append(arr[bounds[0]])
                bounds[0] += 1
        while bounds[0] < orig_right:
            new.append(arr[bounds[0]])
            bounds[0] += 1
        while bounds[1] < stop:
            new.append(arr[bounds[1]])
            bounds[1] += 1
        pos = 0
        for i in range(start, stop):
            arr.write(i, new[pos])
            pos += 1
    wrapper(0, len(arr))

@Sort("Buffered Stooge Sort")
def BufferedStoogeSort(arr):
    def wrapper(start, stop):
        if stop - start > 1:
            if stop - start == 2 and arr.compare(start, stop - 1) == 1:
                arr.swap(start, stop - 1)
            if stop - start > 2:
                third = ceil((stop - start) / 3) + start
                two_third = ceil((stop - start) / 3 * 2) + start
                if two_third - third < third:
                    two_third -= 1
                if not (stop - start - 2) % 3:
                    two_third -= 1
                wrapper(third, two_third)
                wrapper(two_third, stop)
                left, right = third, two_third
                buffer_start = start
                while left < two_third and right < stop:
                    if arr.compare(left, right) == 1:
                        arr.swap(buffer_start, right)
                        right += 1
                    else:
                        arr.swap(buffer_start, left)
                        left += 1
                    buffer_start += 1
                while right < stop:
                    arr.swap(buffer_start, right)
                    right += 1
                    buffer_start += 1
                wrapper(two_third, stop)
                left, right = two_third - 1, stop - 1
                while right > left >= start:
                    if arr.compare(left, right) == 1:
                        for i in range(left, right):
                            arr.swap(i, i + 1)
                        left -= 1
                    right -= 1
    wrapper(0, len(arr))

@Sort("LSD Radix Sort")
def LSDRadixSort(arr, base=2):
    def to_base(n, b):
        if n == 0:
            return [0]
        digits = []
        while n:
            digits.append(int(n % b))
            n //= b
        return digits[::-1]
    incr = min(arr)
    length = len(to_base(max(arr) - incr, base))
    for i in range(length - 1, -1, -1):
        lst = [[] for i in range(base)]
        for j in range(len(arr)):
            num = arr.get(j) - incr
            current = to_base(num, base)
            while len(current) < length:
                current.insert(0, 0)
            arr.append_aux(lst[current[i]], num)
        new = []
        for j in lst:
            new.extend(j)
        for index, j in enumerate(new):
            arr.write(index, j + incr)

@Sort("Bottom-Up Merge Sort")
def BottomUpMergeSort(arr):
    def merge(start, middle, stop):
        aux = []
        left, right = start, middle
        while left < middle and right < stop:
            if arr.compare(left, right) == 1:
                aux.append(arr[right])
                right += 1
            else:
                aux.append(arr[left])
                left += 1
        while left < middle:
            aux.append(arr[left])
            left += 1
        while right < stop:
            aux.append(arr[right])
            right += 1
        return aux
    incr = 1
    while incr < len(arr):
        lst = []
        current = 0
        while current + incr < len(arr):
            stop = incr * 2 + current
            if stop >= len(arr):
                stop = len(arr)
            lst.extend(merge(current, current + incr, stop))
            current += incr * 2
        for index, i in enumerate(lst):
            arr.write(index, i)
        incr *= 2

@Sort("Quick Sort (Left Pivots)")
def QuickSortLeftPivots(arr):
    def wrapper(start, stop):
        if stop - start >= 2:
            left = start + 1
            for right in range(left, stop):
                if arr.compare(start, right) == 1:
                    if left != right:
                        arr.swap(left, right)
                    left += 1
            if start != left - 1:
                arr.swap(start, left - 1)
            wrapper(start, left - 1)
            wrapper(left, stop)
    wrapper(0, len(arr))

@Sort("Selection Merge Sort")
def SelectionMergeSort(arr):
    def wrapper(start, stop):
        if stop - start > 2:
            wrapper(start, (stop - start) // 2 + start)
            wrapper((stop - start) // 2 + start, stop)
        last = (stop - start) // 2 + start + 1
        orig = last - 1
        for i in range(start, stop - 1):
            if orig == i:
                orig += 1
            new = i
            for j in range(orig, last):
                if arr.compare(new, j) == 1:
                    new = j
            if new != i:
                arr.swap(i, new)
                if new == last - 1 and last < stop:
                    last += 1
    wrapper(0, len(arr))

@Sort("Selection Heap Sort")
def SelectionHeapSort(arr):
    def sift_down(start, node):
        left = (node - start) * 2 + 1 + start
        if left < len(arr):
            right = left + 1
            if right < len(arr) and arr.compare(left, right) == 1:
                index = right
            else:
                index = left
            if arr.compare(node, index) == 1:
                arr.swap(node, index)
                sift_down(start, index)
    def heapify(start):
        for node in range(len(arr) - 1, start - 1, -1):
            sift_down(start, node)
    for start in range(len(arr) - 1):
        heapify(start)

@Sort("Max Heap Sort")
def MaxHeapSort(arr):
    MaxHeapified(arr)
    def sift_down(node, stop):
        left = node * 2 + 1
        if left < stop:
            right = left + 1
            if right < stop and arr.compare(left, right) == -1:
                index = right
            else:
                index = left
            if arr.compare(node, index) == -1:
                arr.swap(node, index)
                sift_down(index, stop)
    for node in range(len(arr) - 1, 0, -1):
        arr.swap(0, node)
        sift_down(0, node)

@Sort("Min Heap Sort")
def MinHeapSort(arr):
    MinHeapified(arr)
    def sift_down(node, stop):
        left = node * 2 + 1
        if left < stop:
            right = left + 1
            if right < stop and arr.compare(left, right) == 1:
                index = right
            else:
                index = left
            if arr.compare(node, index) == 1:
                arr.swap(node, index)
                sift_down(index, stop)
    for node in range(len(arr) - 1, 0, -1):
        arr.swap(0, node)
        sift_down(0, node)
    arr.reverse()

@Sort("Cycle Sort")
def CycleSort(arr):   # manual refreshes
    for start in range(len(arr) - 1):
        val = arr[start]
        first = True
        while first or pos != start:
            pos = start
            for i in range(start + 1, len(arr)):
                arr.refresh(start, pos, i)
                if arr.compare_values(val, arr[i], False) == 1:
                    pos += 1
            if first and pos == start:
                break
            while val == arr[pos]:
                pos += 1
                arr.refresh(start, pos)
            first = False
            prev = arr[pos]
            arr.write(pos, val, refresh=False)
            val = prev
            arr.refresh(start, pos)

@Sort("Selection Bogo Sort")
def SelectionBogoSort(arr):
    for i in range(len(arr) - 1):
        while True:
            done = True
            for j in range(i + 1, len(arr)):
                if arr.compare(i, j) == 1:
                    done = False
                    break
            if done:
                break
            arr.swap(i, randrange(i + 1, len(arr)))

@Sort("Sandshaker Sort")
def SandshakerSort(arr):
    left, right = 0, len(arr) - 1
    while True:
        for i in range(right, left, -1):
            if arr.compare(left, i) == 1:
                arr.swap(left, i)
        left += 1
        if left == right:
            break
        for i in range(left, right):
            if arr.compare(i, right) == 1:
                arr.swap(i, right)
        right -= 1
        if left == right:
            break

@Sort("Build-Up Insertion Sort")
def BuildUpInsertionSort(arr):
    for i in range(1, len(arr)):
        for j in range(i):
            arr.step(j, i)

@Sort("Binary Insertion Sort")
def BinaryInsertionSort(arr):
    for i in range(1, len(arr)):
        left, right = 0, i
        while left < right:
            middle = left + ((right - left) // 2)
            comp = arr.compare(middle, i)
            if comp == 1:
                right = middle
            elif comp == -1:
                left = middle + 1
            else:
                left = right = middle
        for j in range(i, left, -1):
            arr.swap(j - 1, j)

@Sort("Stable Binary Insertion Sort")
def StableBinaryInsertionSort(arr):
    for i in range(1, len(arr)):
        left, right = 0, i
        while left < right:
            middle = left + ((right - left) // 2)
            if arr.compare(middle, i) == 1:
                right = middle
            else:
                left = middle + 1
        for j in range(i, left, -1):
            arr.swap(j - 1, j)

@Sort("Unsorted Binary Insertion Sort")
def UnsortedBinaryInsertionSort(arr):
    def bin_search(stop):
        left, right = 0, stop
        while left < right:
            middle = left + ((right - left) // 2)
            if arr.compare(middle, stop) == 1:
                right = middle
            else:
                left = middle + 1
        for i in range(stop, left, -1):
            arr.swap(i - 1, i)
        return left
    done = False
    while not done:
        done = True
        current = len(arr) - 1
        while current:
            if bin_search(current) == current:
                current -= 1
            else:
                done = False

@Sort("Quick Sort (Average Pivots)")
def QuickSortAveragePivots(arr):
    def wrapper(start, stop):
        length = stop - start
        if length >= 2:
            average = 0
            for i in range(start, stop):
                average += arr.get(i)
            left = start
            swap = False
            for right in range(start, stop):
                arr.refresh(right)
                arr.incr_comps()
                if average > arr[right] * length:
                    if left != right:
                        arr.swap(left, right)
                    swap = True
                    left += 1
            if swap:   # prevents softlock on no unique
                wrapper(start, left)
                wrapper(left, stop)
    wrapper(0, len(arr))

@Sort("Partition Merge Sort")
def PartitionMergeSort(arr):   # only works on power of 2 lengths, linear dist
    def partition(start, stop):
        length = stop - start
        if length >= 2:
            average = 0
            for i in range(start, stop):
                average += arr.get(i)
            left = start
            for right in range(start, stop):
                arr.refresh(right)
                arr.incr_comps()
                if average > arr[right] * length:
                    if left != right:
                        arr.swap(left, right)
                    left += 1
    def pairwise(buffer, left, right):
        comp = arr.compare(left, right)
        if comp == 1:
            arr.swap(buffer, right)
            arr.swap(buffer + 1, left)
        else:
            arr.swap(buffer, left)
            arr.swap(buffer + 1, right)
    def first_merges(buffer, stop):
        while buffer + 3 < stop:
            left = buffer + 2
            right = left + 1
            pairwise(buffer, left, right)
            buffer += 2
    def merge(buffer, left, right, stop):
        orig_left, orig_right = left, right
        while left < orig_right and right < stop:
            if arr.compare(left, right) == 1:
                arr.swap(buffer, right)
                right += 1
            else:
                arr.swap(buffer, left)
                left += 1
            buffer += 1
        while right < stop:
            arr.swap(buffer, right)
            right += 1
            buffer += 1
    def merges(buffer_start, buffer_stop, stop):
        diff = buffer_stop - buffer_start
        while buffer_start + (diff * 4) - 1 < stop:
            merge(buffer_start, buffer_stop, buffer_stop + diff, buffer_stop
                + (diff * 2))
            buffer_start += diff * 2
            buffer_stop += diff * 2
    def merge_back(stop, left, right, buffer):
        orig_left, orig_right = left, right
        while left > stop and right > orig_left:
            if arr.compare(left, right) == -1:
                arr.swap(right, buffer)
                right -= 1
            else:
                arr.swap(left, buffer)
                left -= 1
            buffer -= 1
        while left > stop:
            arr.swap(left, buffer)
            left -= 1
            buffer -= 1
    def wrapper(buffer, start, stop):
        if buffer == start:
            arr.step(start, stop)
            arr.step(start + 1, stop + 1)
            arr.step(start, stop)
        else:
            partition(0, stop)
            first_merges(start - 2, stop)
            current = start - 4
            step = 2
            while current >= buffer:
                merges(current, current + step, stop)
                step *= 2
                current -= step
            merge_back(buffer - 1, start - 1, buffer + start - 1, stop - 1)
            wrapper(buffer // 2, buffer, start)
    length = len(arr)
    wrapper(length // 4, length // 2, length)

@Sort("New Partition Merge Sort")
def NewPartitionMergeSort(arr):
    def partition(stop):
        average = 0
        for i in range(stop):
            average += arr.get(i)
        left = 0
        for right in range(stop):
            arr.refresh(right)
            arr.incr_comps()
            if average > arr[right] * stop:
                if left != right:
                    arr.swap(left, right)
                left += 1
        return left
    def pairwise(buffer, left, right):
        comp = arr.compare(left, right)
        if comp == 1:
            arr.swap(buffer, right)
            arr.swap(buffer + 1, left)
        else:
            arr.swap(buffer, left)
            arr.swap(buffer + 1, right)
    def pairwise_swaps(buffer):
        while buffer + 3 < len(arr):
            pairwise(buffer, buffer + 2, buffer + 3)
            buffer += 2
        if buffer < len(arr) - 2:
            arr.swap(buffer, buffer + 2)
    print(partition(len(arr)))
    pairwise_swaps(len(arr) // 2 - 2)

@Sort("Bitonic Sort")
def BitonicSort(arr):
    direction = True
    maximum = 1
    length = len(arr)
    while maximum < length:
        max_times_2 = maximum * 2
        change = maximum < length // 2
        gap = maximum
        while gap:
            for start in range(0, length, gap * 2):
                if start % max_times_2 == 0 and change:
                    direction = not direction
                for current in range(start, start + gap):
                    if direction:
                        arr.step(current, current + gap)
                    else:
                        arr.step(current + gap, current)
            gap //= 2
        maximum *= 2

@Sort("Odd Even Merge Sort")
def OddEvenMergeSort(arr):
    n = len(arr)
    p = 1
    while p < n:
        k = p
        while k:
            for j in range(k % p, n - k, 2 * k):
                for i in range(k):
                    if int((i + j) / (p * 2)) == int((i + j + k) / (p * 2)):
                        arr.step(i + j, i + j + k)
            k //= 2
        p *= 2

@Sort("Recursive Pop Sort")
def RecursivePopSort(arr):
    def wrapper(start, stop, direction):
        if stop - start >= 2:
            wrapper(start, (stop - start) // 2 + start, not direction)
            wrapper((stop - start) // 2 + start, stop, direction)
            right = stop - 1
            while True:
                if direction:
                    while right > start and arr.compare(start, right) == -1:
                        right -= 1
                else:
                    while right > start and arr.compare(start, right) == 1:
                        right -= 1
                if right == start:
                    break
                for i in range(start, right):
                    arr.swap(i, i + 1)
                right -= 1
    wrapper(0, len(arr), True)

@Sort("MSD Radix Sort")
def MSDRadixSort(arr, base=2):
    def to_base(n, b):
        if n == 0:
            return [0]
        digits = []
        while n:
            digits.append(int(n % b))
            n //= b
        return digits[::-1]
    def wrapper(start, stop, digit):
        if stop - start >= 2 and digit < length:
            lst = [[] for i in range(base)]
            for i in range(start, stop):
                num = arr.get(i) - incr
                new = to_base(num, base)
                while len(new) < length:
                    new.insert(0, 0)
                lst[new[digit]].append(num)
            extended = []
            for i in lst:
                extended.extend(i)
            index = start
            for i in extended:
                arr.write(index, i + incr)
                index += 1
            pos = start
            for i in lst:
                wrapper(pos, pos + len(i), digit + 1)
                pos += len(i)
    incr = min(arr)
    length = len(to_base(max(arr) - incr, base))
    wrapper(0, len(arr), 0)

@Sort("No-Heap Max Heap Sort")
def NoHeapMaxHeapSort(arr):
    def sift_down(node, start, stop):
        left = (node - start) * 2 + 1 + start
        if left < stop:
            right = left + 1
            if right < stop:
                child = right if arr.compare(left, right) == -1 else left
            else:
                child = left
            if arr.compare(node, child) == -1:
                arr.swap(node, child)
                sift_down(child, start, stop)
    def pseudo_sort(start):
        for i in range(len(arr) - 1, start, -1):
            arr.swap(start, i)
            sift_down(start, start, i)
    for i in range(len(arr) - 1):
        pseudo_sort(i)
    if len(arr) >= 2:
        if arr.compare(1, 2) == 1:
            arr.swap(1, 2)
        else:
            arr.step(0, 1)

@Sort("Selection Pancake Sort")
def SelectionPancakeSort(arr):
    for i in range(len(arr) - 1):
        smallest = arr.get_min(i)
        if smallest != i:
            arr.reverse(i, smallest + 1)

@Sort("Recursive Shell Sort")
def RecursiveShellSort(arr):
    def insertion(start, stop, gap):
        for i in range(start, stop - gap, gap):
            while i >= start and arr.compare(i, i + gap) == 1:
                arr.swap(i, i + gap)
                i -= gap
    def wrapper(start, gap):
        if gap + start <= len(arr):
            wrapper(start, gap * 2)
            wrapper(start + gap, gap * 2)
            insertion(start - 1, len(arr), gap)
    wrapper(1, 1)

@Sort("Iterative Pairwise Sort")
def IterativePairwiseSort(arr):
    n = len(arr)
    a = 1
    while a < n:
        b = a
        c = 0
        while b < n:
            arr.step(b - a, b)
            b += 1
            c = (c + 1) % a
            if not c:
                b += a
        a *= 2
    a //= 4
    e = 1
    while a:
        d = e
        while d:
            b = (d + 1) * a
            c = 0
            while b < n:
                arr.step(b - d * a, b)
                c = (c + 1) % a
                b += 1
                if not c:
                    b += a
            d //= 2
        a //= 2
        e = e * 2 + 1

@Sort("Pancake Sort")
def PancakeSort(arr):
    for i in range(len(arr) - 1, 0, -1):
        index = arr.get_max(0, i + 1)
        if index != i:
            if index != 0:
                arr.reverse(0, index + 1)
            arr.reverse(0, i + 1)

@Sort("Base N Max Heap Sort")
def BaseNMaxHeapSort(arr, base=3):
    def sift_down(node, stop):
        left = node * base + 1
        if left < stop:
            max_index = left
            for i in range(left + 1, left + base):
                if i >= stop:
                    break
                if arr.compare(max_index, i) == -1:
                    max_index = i
            if arr.compare(node, max_index) == -1:
                arr.swap(node, max_index)
                sift_down(max_index, stop)
    for i in range(len(arr) - 1, -1, -1):
        sift_down(i, len(arr))
    for i in range(len(arr) - 1, 0, -1):
        arr.swap(0, i)
        sift_down(0, i)

# ------------------------------------------------------------------------------

def ON_START_UP():
    "Use this to auto-import scripts or set new defaults for GUI elements."
    shuffle_selected.set("Random Unique")
    s_dropdown.config(state="normal")
    global shuffle_bool
    shuffle_bool = True

try:
    ON_START_UP()
except:
    showerror("Start Up", "Traceback in ON_START_UP:\n%s" % format_exc())
    sys.stderr.write("Traceback in ON_START_UP:\n%s" % format_exc()[35:])

root.update()

if HIDE_PYGAME:
    os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
try:
    from numpy import sin, pi, arange, float32
    from pygame.mixer import init, Sound
    from scipy.signal import square
    init(channels=1)
    use_sound.config(state="normal")
except:
    showerror("Loading Sound", "Sound could not be loaded:\n%s" % format_exc())
    sys.stderr.write("Traceback in loading sound:\n%s" % format_exc()[35:])

if LOAD_ICON:
    try:
        from PIL import Image, ImageTk
        root.iconphoto(False, ICON if ICON_FROMFILE else \
                       ImageTk.PhotoImage(Image.open(BytesIO(ICON))))
    except:
        showerror("Loading Image", "Icon image could not be loaded:\n%s"
                  % format_exc())
        sys.stderr.write("Traceback in loading image:\n%s" % format_exc()[35:])

root.title("_fluffyy's Sorting Visualizer - %s Sorting Algorithms" % len(sorts))
root.mainloop()
