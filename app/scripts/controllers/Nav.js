'use strict';

angular.module('cupidCrawlerApp')
  .controller('NavCtrl', function ($scope, $http) {
    
    // Get crawl status
    $scope.getCrawlStatus = function() {
      $http({
        url: "/api/is-crawling",
        method: "GET"
      }).success(function(data, status, headers, config) {
        if (data.status) {
          $scope.isCrawling = true;
        } else {
          $scope.isCrawling = false;
        }
      }).error(function(data, status, headers, config) {
        $scope.status = status;
      });
    }

    // Crawl modal
    $scope.openCrawlModal = function() {
      $scope.getCrawlStatus();
      $scope.crawlModalShouldBeOpen = true;
    };

    $scope.closeCrawlModal = function() {
      $scope.crawlModalShouldBeOpen = false;
    };

    $scope.crawlModalOpts = {
      backdropFade: true,
      dialogFade: true
    };

    $scope.startCrawl = function() {
      $http({
        url: "/crawlstarter/10",
        method: "GET"
      }).success(function(data, status, headers, config) {
        $scope.getCrawlStatus();
      }).error(function(data, status, headers, config) {
        $scope.status = status;
      });
    };
    
  });
