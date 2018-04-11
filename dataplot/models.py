from django.db import models


class site_info(models.Model):
    ## Information about the site goes here.
    # Type of site - eg, AURN, China, GAUGE etc.
    site_type = models.CharField(max_length = 50)
    ## Need the site code
    site_code = models.CharField(max_length = 20, unique = True)
    site_name = models.CharField(max_length = 100, unique = True)
    ## Site coords
    latitude = models.FloatField()
    longitude = models.FloatField()
    altitude = models.FloatField(null = True)
    # Site address (country relevant, address maybe only for AURN)
    country = models.CharField(max_length = 100, null = True)
    address = models.CharField(max_length = 300, null = True)
    # Region and environment type is mainly for AURN
    region = models.CharField(max_length = 300, null = True)
    environment_type = models.CharField(max_length = 300, null = True)
    EU_site_ID  = models.CharField(max_length = 50, null = True)
    UK_AIR_ID = models.CharField(max_length = 50, null = True)
    # When was the site open to and from
    site_open = models.NullBooleanField(default = None)
    date_open = models.DateField(null = True)
    date_closed = models.DateField(null = True)
    # # A list of the availble species at the site?
    # # Not sure how to do that
    # pollutants_measured = models.ManyToMany(pollutants_details)

    def __str__(self):
        return self.site_code

class pollutants_details(models.Model):
    pollutant_name = models.CharField(max_length = 100,null = True)
    start_date = models.DateField(null = True)
    end_date = models.DateField(null = True)
    relevant_site = models.ForeignKey(site_info, on_delete = models.CASCADE)

    def __str__(self):
        return self.pollutant_name

class measurement_info(models.Model):
    ## Information about the variables measured
    variable_name = models.CharField(max_length = 100)
    unit = models.CharField(max_length = 100)
    chemical_formula = models.CharField(max_length = 100)
     # Could add AQ limit at some point
    measurement_name = models.CharField(max_length = 100, unique = True)

    def __str__(self):
        return self.measurement_name

# Test to see if we can make database for AURN data
class measurement_data(models.Model):
    ## Need each obsveration to have:
    # Date and time
    date_and_time = models.DateTimeField()
    # An actual value
    value = models.FloatField()
    # Validated
    VERIFIED_CHOICES = (
        ('V','Verified'),
        ('P','Priliminary Verified'),
        ('N','Not Verified'),
        ('U','Unknown')
    )
    verified = models.CharField(max_length = 1, choices = VERIFIED_CHOICES)
    # Site identifer
    site_id = models.ForeignKey(site_info, on_delete = models.PROTECT)
    # Measurement identifer
    measurement_id = models.ForeignKey(measurement_info, on_delete = models.CASCADE)

    def __str__(self):
        return 'Measurement no: %s' % str(self.id)
