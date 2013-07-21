'use strict';

angular.module('cupidCrawlerApp')
  .filter('locationFilter', function () {
    return function (profiles, locations) {
      var result = [];
      angular.forEach(profiles, function(profile) {
        if (locations[profile.location]) {
          this.push(profile);
        }
      }, result);
      return result;
    };
  });