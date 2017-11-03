**Trabd** (Arabic for _association_) is a free-software student
election platform, hosted at https://trabdportal.com.

# Installation

Trabd is designed to work with Python 2.7 and Django 1.11.

To start your instance, clone this repository:
```
git clone https://github.com/SAlkhairy/trabd.git
cd trabd
```

Then copy `fudul/secrets.template.py` to `fudul/secrets.py` and set
the `SECRET_KEY` variable using [this tool](http://www.miniwebtool.com/django-secret-key-generator/).

Then install the requirements, set up the database by running the
following commands:

```
# Install the requirements:
pip install --user -r requirements.txt
# Set up the database:
python manage.py migrate
# Load initial data:
python manage.py loaddata voting/fixtures/default_positions.json
# Prepare basic permissions:
python manage.py check_permissions
```

That's it!

# Licensing

* Copyright (C) 2017 Saleha Alkhairy
* Copyright (C) 2017 [Osama Khalid](https://osamakhalid.com)

```
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Affero General Public License for more details.
```
