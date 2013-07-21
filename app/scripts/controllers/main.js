'use strict';

angular.module('cupidCrawlerApp')
  .controller('MainCtrl', function ($scope, $http) {
   
    $scope.profiles;
    $scope.profilesStatus = 'WAITING';
    $scope.profilesCount = -1;
    $scope.filtered = 0;

    $http({
      url: "/api/profiles",
      method: "GET"
    }).success(function(data, status, headers, config) {
      $scope.profiles = data.data;
      $scope.profilesStatus = data.status;
      $scope.profilesCount = data.count;
      
      // Location
      $scope.locations = [];
      $scope.selectedLocations = {};

      // Age
      $scope.ages = [];
      $scope.selectedAges = {};
      $scope.ageRange = {
        'minAge': undefined,
        'maxAge': undefined
      };

      // Ethnicity
      $scope.ethnicities = [];
      $scope.selectedEthnicities = {};

      // Body Type
      $scope.bodyTypes = [];
      $scope.selectedBodyTypes = {};

      // For Loop
      angular.forEach($scope.profiles, function(item){
        // Build the img list
        var img_more_list = [];
        for (var i = 0; i < item.img_more.length; i++) {
          var img_more_data = {
            'url': item.img_more[i],
            'caption': item.img_more_captions[i]
          }
          img_more_list.push(img_more_data);
        }
        // item.img_more = img_more_list;
        var split_img_list = item.img_more.split("'");
        var split_caption_list = item.img_more_captions.split("'");
        img_more_list = [];
        for (var i = 1; i < split_img_list.length; i++) {
          if (i % 2 == 1) {
            var img_more_data = {
              'url': split_img_list[i],
              'caption': split_caption_list[i],
              'selected': false
            }
            img_more_list.push(img_more_data);
          }
        }
        item.img_more = img_more_list;

        // Location
        if (!$scope.selectedLocations[item.location]) {
          var locationData = {
            'name': item.location,
            'checked': true,
            'count': 1
          }
          $scope.selectedLocations[item.location] = true;
          $scope.locations.push(locationData);
        } else {
          $.grep($scope.locations, function(e){return e.name == item.location})[0]['count']++;
        }

        // Age
        if ($scope.ages.indexOf(item.age) == -1) {
          var ageData = {
            'age': item.age,
          }
          $scope.ages.push(item.age);
        }

        if ($scope.ageRange.minAge == undefined || item.age < $scope.ageRange.minAge) {
          $scope.ageRange.minAge = item.age;
          $scope.minAgeStatic = item.age;
        }
        if ($scope.ageRange.maxAge == undefined || item.age > $scope.ageRange.maxAge) {
          $scope.ageRange.maxAge = item.age;
          $scope.maxAgeStatic = item.age;
        }

        // Ethnicity
        var ethnicityProperty = item.ethnicity;
        var ethnicities = ethnicityProperty.split(',');
        angular.forEach(ethnicities, function(property) {
          property = property.trim();
          if (!$scope.selectedEthnicities[property]) {
            var ethnicityData = {
              'ethnicity': property,
              'checked': true,
              'count': 1
            }
            $scope.selectedEthnicities[property] = true;
            $scope.ethnicities.push(ethnicityData);
          } else {
            $.grep($scope.ethnicities, function(e){return e.ethnicity == property})[0]['count']++;
          }
        });

        // Body type
        if (!$scope.selectedBodyTypes[item.body_type]) {
          var bodyTypeData = {
            'type': item.body_type,
            'checked': true,
            'count': 1
          }
          $scope.selectedBodyTypes[item.body_type] = true;
          $scope.bodyTypes.push(bodyTypeData);
        } else {
          $.grep($scope.bodyTypes, function(e){return e.type == item.body_type})[0]['count']++;
        }

      });
      
    }).error(function(data, status, headers, config) {
      $scope.status = status;
    });

    $scope.selectAll = function(type, all) {
      for (var key in type) {
        type[key] = all;
      }
    };

    $scope.allSelected = function(type, all) {
      if (all) {
        for (var key in type) {
          if (!type[key]) 
            return false;
        }
        return true;
      } else {
        for (var key in type) {
          if (type[key]) {
            return false;
          }
        }
        return true;
      }
    };

    

  });
