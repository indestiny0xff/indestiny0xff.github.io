---
layout: page
title: Blog Archive
---

![](https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExMm4xMW1pdmYwZzJiOHB6bHdqZmE1N3cxcWdkMHFhYWN5Yzh5MW9ibyZlcD12MV9naWZzX3NlYXJjaCZjdD1n/FrqU6wyZWRUQqpISRt/200.webp)


{% for tag in site.tags %}
  <h3>{{ tag[0] }}</h3>
  <ul>
    {% for post in tag[1] %}
      <li><a href="{{ post.url }}">{{ post.date | date: "%B %Y" }} - {{ post.title }}</a></li>
    {% endfor %}
  </ul>
{% endfor %}
