'use strict';

angular.module('cupidCrawlerApp')
  .filter('ethnicityFilter', function () {
    return function (profiles, ethnicities) {
      var result = [];
      var resultUsernames = {};
      angular.forEach(profiles, function(profile) {
        var ethnicityProperty = profile.ethnicity;
        var ethnicityProperties = ethnicityProperty.split(',');
        angular.forEach(ethnicityProperties, function(property) {
          property = property.trim();
          if (ethnicities[property] && !resultUsernames[profile.username]) {
            resultUsernames[profile.username] = true;
            result.push(profile);
          }
        });
      });
      return result;
    };
  });
