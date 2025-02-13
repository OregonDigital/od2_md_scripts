from Od2Package import Package
import sys

try:
    custom = sys.argv[1]
except:
    custom = None

package = Package(custom)
print(package.custom)
# ...
