<h1>Scraper for euronics web store</h1>
<p>
This is basic webscraper made with Selenium.
It searches Euronics website (Estonian tech store) for products with given criteria and gets their price statistics.
When used right, this programme will display minimal, maximum and average prices for the given product.

When launching this code first you need to enter the name of the product. For example iphone 12.
After that you need to enter the category to which this product belongs.
It is suggerted to use these names when searching:
</p>
<ul>
<li> smartphone </li>
<li> tablet </li>
<li> notebook </li>
<li> monitor </li>
<li> smartwatch and so on </li>
</ul>
<p>
I suggest using these keywords because in this case Euronics website gives more accurate results and possibility of seing unexpected product decreases.
You can also launch this code from the terminal. For shell scripting use this
</p>
<code>
#!/bin/zsh </code><br>
<code> cd {directory in which the python file is saved}</code> <br>
<code> python3 priceScraper.py
</code>
