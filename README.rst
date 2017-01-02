Armatis
=======

.. image:: https://img.shields.io/badge/License-BSD%202--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-2-Clause
.. image:: https://badge.fury.io/py/armatis.svg
   :target: https://badge.fury.io/py/armatis
.. image:: https://travis-ci.org/iBluemind/armatis.svg?branch=master
   :target: https://travis-ci.com/iBluemind/armatis
.. image:: https://readthedocs.org/projects/armatis/badge/
   :target: http://armatis.readthedocs.io/en/latest/

Armatis parses the website or web API response of Korean
parcel delivery service company for tracking the parcel.

Installation
------------

Install Armatis with this following command:

.. code:: sh

    $ pip install armatis

Usage
-----

Armatis is simple to use. Just need to type the delivery company code
and the invoice number.

To find the parcel, just use the method ``find()``:

.. code:: python

    from armatis import Armatis

    tracker = Armatis('cj', 123456789123)
    tracker.find()

You can use the method ``supported_companies()`` to find the supported
delivery company names and company codes.

.. code:: python

    tracker.supported_companies()

The returned data of the method ``find()`` is like below:

.. code:: json

    {
        "company": {
            "contact": "1588-1255",
            "name": "CJ대한통운"
        }, 
        "parcel": {
            "receiver": "(주*",
            "sender": "한만*",
            "note": "일반",
            "address": "경기도 성남시 분당구******"
        },
        "tracks": [
            {
                "time": "2016-10-13 18:07:13",
                "status": "간선상차",
                "location": "파주Sub",
                "phone1": "파주Sub(031-960-6566)",
                "phone2": null
            },
            {
                "time": "2016-10-13 21:22:09",
                "status": "집화처리",
                "location": "경기파주",
                "phone1": "경기파주(070-7779-1003)",
                "phone2": null
            },
            {
                "time": "2016-10-14 02:06:39",
                "status": "간선하차",
                "location": "옥천HUB",
                "phone1": null,
                "phone2": null
            }, 
            {
                "time": "2016-10-14 02:17:16",
                "status": "간선하차",
                "location": "옥천HUB",
                "phone1": null,
                "phone2": null
            }, 
            {
                "time": "2016-10-14 02:25:10",
                "status": "행낭포장",
                "location": "옥천HUB",
                "phone1": null,
                "phone2": null
            }, 
            {
                "time": "2016-10-14 04:06:49",
                "status": "간선상차",
                "location": "옥천HUB",
                "phone1": null,
                "phone2": null
            },
            {
                "time": "2016-10-14 11:10:05",
                "status": "간선하차",
                "location": "분당A",
                "phone1": "분당A(031-725-9222)",
                "phone2": null
            },
            {
                "time": "2016-10-14 11:12:07",
                "status": "배달출발",
                "location": "분당대리점a(C15F)",
                "phone1": "분당대리점a(C15F)(031-769-0516)",
                "phone2": "01012345678"
            },
            {
                "time": "2016-10-14 16:44:35",
                "status": "배달완료",
                "location": "분당대리점a(C15F)",
                "phone1": "분당대리점a(C15F)(031-769-0516)",
                "phone2": "01012345678"
            }
        ]
    }

Supported Delivery Companies
----------------------------

The following delivery companies are supported currently.

+--------------------+----------------+----------------+
| Company            | Test existed   | Last Updated   |
+====================+================+================+
| CJ대한통운         | o              | 2016-12-10     |
+--------------------+----------------+----------------+
| 로젠택배           | o              | 2016-12-10     |
+--------------------+----------------+----------------+
| 현대택배           | o              | 2016-12-10     |
+--------------------+----------------+----------------+
| 한진택배           | o              | 2016-12-10     |
+--------------------+----------------+----------------+
| KG로지스           | o              | 2016-12-10     |
+--------------------+----------------+----------------+
| CVSNet편의점택배   |                | 2014-10-19     |
+--------------------+----------------+----------------+
| GTX로지스          | o              | 2017-01-02     |
+--------------------+----------------+----------------+
| 우체국택배         |                | 2014-10-19     |
+--------------------+----------------+----------------+
| 합동택배           |                | 2014-10-19     |
+--------------------+----------------+----------------+
| EMS                | o              | 2017-01-02     |
+--------------------+----------------+----------------+
| KGB택배            | o              | 2017-01-02     |
+--------------------+----------------+----------------+

How to add new company
----------------------

You can make the new delivery company parser easily.

First, create a class which inherit ``Parser``, and implement the method
``parse()``.

.. code:: python

    from armatis.models import Parcel, Track
    from armatis.parser import Parser, ParserRequest

    class NewCompanyParser(Parser):
        def __init__(self, invoice_number, config):
            super(NewCompanyParser, self).__init__(invoice_number, config)
            # Describe the information about the website or web API provided by the delivery company 
            parser_request = ParserRequest(url='http://thecompany.co.kr/tracking?invno=%s' % self.invoice_number)
            self.add_request(parser_request)
            
        # Actually occurred parsing the website or web API provided above 
        def parse(self, parser):
            tables = parser.find_all('tbody')

            parcel = Parcel()
            parcel.sender = ...         # Sender's name
            parcel.receiver = ...       # Receiver's name
            parcel.address = ...        # Receive address
            parcel.note = ...           # Describe about the parcel
            self.parcel = parcel        # Store the information about the parcel!

            trs = tables[1].find_all('tr')
            for tr in trs:
                track = Track()
                track.status = ...      # Status of the delivery history
                track.time = ...        # Time of the delivery history
                track.location = ...    # Location the parcel where it is 
                track.phone1 = ...      # Contact of the location
                track.phone2 = ...      # Contact of the location
                self.add_track(track)   # Add the tracking information!

| And, make a ``Company`` instance that describe the company.
| Finally, register this ``Company`` object with the ``Parser`` class
  you made above.

.. code:: python

    from armatis import Armatis, Company

    tracker = Armatis()

    # Make a Company instance that describe the company
    the_new_company = Company('새로운회사', 'nc', '1234-5678', [10, 12])
    # Register the Company object with the Parser class you made
    tracker.parser_manager.register_parser(the_new_company, NewCompanyParser)

Documentation
-------------

Completed documentation for Armatis is available on
`ReadtheDocs <http://armatis.readthedocs.io/en/latest/>`__.

Contributing
------------

Welcome contributions! If you would like to contribute on Armatis,
please follow these steps:

1. Fork this repository
2. Make your changes
3. Install the requirements using ``pip install -r requirements.txt``
4. Submit a pull request after running ``make ready``
