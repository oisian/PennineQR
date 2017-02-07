#$a = 0;
#for ($x = 1; $x < $this->level() + 1; $x++) {
#$a += floor($x + 200 * pow(2, ($x / 7)));
#}
#return floor($a / 4);

import math

a = 0
level = 2
x = 1
level = level + 1

while True:
    if x == 99:
        break
    a = math.floor((x + 200 * pow(2,(x/7))))
    print(math.floor(a / 4))
    x += 1
    level += 1