# PyFCG

*A Python interface to FCG and Babel, built on FCG Go.*

## Installation

To install this package from PyPI, run the following command.

```bash
pip install pyfcg
```

## Use

Start a PyFCG session with:

```
import pyfcg as fcg
fcg.init(port=9600)
```

This starts up FCG Go, listening at port 9600.

Then:

```
fcg.load_demo_grammar()
fcg.start_web_interface(port=8010,open=True)
fcg.activate_monitors(['trace-fcg'])
fcg.comprehend("the linguist likes the mouse", grammar='*fcg-constructions*')
```

And you can enjoy everything at http://localhost:8010 !

## Documentation

Full documentation of this package, including examples can be found on [pyfcg.readthedocs.io](https://pyfcg.readthedocs.io).