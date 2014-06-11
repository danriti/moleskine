# python-traceview: A library for accessing the TraceView API

Not to long ago, we introduced the [TraceView Data API][1], which exposes high
level metrics and performance data related to your TraceView account via a
[RESTful][9] API. For the unfamiliar, this means you can access
[server latency timeseries][5], [application error rates][6], and even
[browsers used by end users][7].

In an effort to make accessing the Data API even easier, I have a created
[python-traceview][2], an open source Python library for easy access to the
TraceView Data API!

## Installation

With support for Python 2.7, 3.2, 3.3, and 3.4, install **python-traceview**
by simply:

```bash
$ pip install python-traceview
```

If you don't have Python installed, I recommend this [guide][10] for
installation instructions and best practices.

## Getting Started

Begin by importing the ``traceview`` module:

```python
>>> import traceview
```

Now, let's initialize a `TraceView` object using your TraceView access (API)
key. You can find this key on the **Organization Overview** page in TraceView:

```python
>>> tv = traceview.TraceView('API KEY HERE')
```

Now, we have a `TraceView` object called ``tv``. We can get all the information
we need from this object.

For example, let's get all available applications setup within your TraceView
account:

```python
>>> tv.apps()
[u'Default', u'pyramid_web_app']
```

Nice, right? We can also get a server side latency summary for the ``Default``
application:

```python
>>> tv.server.latency_summary(app='Default', time_window='hour')
{u'count': 2746.0, u'average': 213911.87181354698, u'latest': 35209.87654320987}
```

TraceView has traced 2746 requests in the last hour, with an average latency of
213ms. Not bad, now let's examine what application layers are available in the
`Default` application:

```python
>>> tv.layers('Default')
[u'PHP', u'cURL', u'file_get_contents', u'lighttpd', u'php_mysql', u'php_mysqli']
```

Finally, let's look at a more advanced example. Using the powerful
[matplotlib][11] library, let's create a [script][13] for graphing the average
latency of the `PHP` layer over the past week:

```python
from datetime import datetime

import matplotlib.pyplot as plt
import traceview

API_KEY = 'API KEY HERE'

def main():
    tv = traceview.TraceView(API_KEY)
    results = tv.server.latency_by_layer('Default', time_window='week')

    # get the php layer dictionary
    php = next((x for x in results if x.get('layer') == 'PHP'), None)

    # convert timestamps to datetime objects
    dates = [datetime.utcfromtimestamp(i[0]) for i in php['timeseries']['items']]

    # calculate average latency and convert to milliseconds
    average_latency = [((i[2] / i[1]) / 1000) for i in php['timeseries']['items']]

    # create a matplotlib plot
    plt.figure(figsize=(12, 5), dpi=80)
    plt.plot(dates, average_latency)
    plt.title('PHP Average Latency (ms) - by Week')
    plt.savefig('latency.png')

if __name__ == '__main__':
    main()
```

![php average latency by week][12]

## Conclusion

For more information, check out the [documentation][3], create an [issue][8], or
leave a comment on what other information you'd like to see available via the
Data API!

[1]: http://www.appneta.com/blog/data-api-for-web-application-monitoring/
[2]: https://github.com/danriti/python-traceview
[3]: http://python-traceview.readthedocs.org/
[4]: http://dev.appneta.com/docs/api-v2/reference.html
[5]: http://dev.appneta.com/docs/api-v2/latency.html#endpoints
[6]: http://dev.appneta.com/docs/api-v2/errors.html#error-rate
[7]: http://dev.appneta.com/docs/api-v2/discovery.html#browsers
[8]: https://github.com/danriti/python-traceview/issues/new
[9]: http://en.wikipedia.org/wiki/Representational_state_transfer
[10]: http://docs.python-guide.org/en/latest/dev/virtualenvs/
[11]: http://matplotlib.org/
[12]: https://raw.githubusercontent.com/danriti/moleskine/master/python-traceview/images/latency.png
[13]: https://gist.github.com/danriti/f93c88522fb17eb1d4a1
