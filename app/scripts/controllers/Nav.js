'use strict';

angular.module('cupidCrawlerApp')
  .controller('NavCtrl', function ($scope, $http) {
    
    $scope.userInfo;

    // Get crawl status
    $scope.getCrawlStatus = function() {
      $http({
        url: "/api/user-info",
        method: "GET"
      }).success(function(data, status, headers, config) {
        $scope.userInfo = data;
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
      dialogFade: true,
      dialogClass: 'modal crawl-dialog',
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

    $scope.logout = function() {
      window.location.href = window.location.href.split('/')[0] + '/logout';
    };
    
  });
