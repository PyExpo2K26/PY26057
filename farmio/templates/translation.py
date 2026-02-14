<h3>
    {% if session['lang'] == 'Tamil' %} 
        விவசாயி உள்நுழைவு 
    {% elif session['lang'] == 'Hindi' %}
        किसान लॉगिन
    {% else %}
        Farmer Login
    {% endif %}
</h3>