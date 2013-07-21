'use strict';

// angular.module('cupidCrawlerApp')
//   .filter('ageFilter', function () {
//     return function (profiles, ages) {
//       var result = [];
//       angular.forEach(profiles, function(profile) {
//         if (ages[profile.age]) {
//           this.push(profile);
//         }
//       }, result);
//       return result;
//     };
//   });

angular.module('cupidCrawlerApp')
  .filter('ageFilter', function () {
    return function (profiles, ages) {
      var result = [];
      angular.forEach(profiles, function(profile) {
        if (profile.age >= ages['minAge'] && profile.age <= ages['maxAge']) {
          this.push(profile);
        }
      }, result);
      return result;
    };
  });
