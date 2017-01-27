---
layout: default
---
## Most 'required' packages in PyPi distributions
<ol>
{% for package in site.data._popular %}
  <li>
    <a href="/package/?{{package[0]}}">
      {{ package[0] }} -- referenced by {{package[1].size}} of packages
    </a>
  </li>
{% endfor %}
</ol>