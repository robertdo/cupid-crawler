'use strict';

angular.module('cupidCrawlerApp')
  .filter('bodyTypeFilter', function () {
    return function (profiles, bodyTypes) {
      var result = [];
      angular.forEach(profiles, function(profile) {
        if (bodyTypes[profile.body_type]) {
          this.push(profile);
        }
      }, result)
      return result;
    };
  });
