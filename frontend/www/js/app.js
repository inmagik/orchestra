(function(){
    'use strict';
  angular.module('Orchestra', ['ui.router', 'drfAuth', 'LocalStorageModule', 'OrchestraServer'])

  .config(['$httpProvider', 'DrfConfigProvider', '$stateProvider', '$urlRouterProvider',
    function($httpProvider, DrfConfigProvider, $stateProvider, $urlRouterProvider) {

      //CORS CONFIGURATION
      $httpProvider.defaults.useXDomain = true;
      delete $httpProvider.defaults.headers.common['X-Requested-With'];

      //AUTH CONFIGURATION
      DrfConfigProvider.setLoginUrl('http://localhost:8000/api-token-auth/');
      DrfConfigProvider.setMode('token');


      //ROUTER CONFIGURATION
      $urlRouterProvider.otherwise("/dashboard");

      // Now set up the states
      $stateProvider
        .state('dashboard', {
          url: "/dashboard",
          templateUrl: "templates/dashboard.html"
        })

        .state('meta_workflows', {
          url: "/meta-workflows",
          templateUrl: "templates/meta_workflows.html",
          controller  :'WfMetaCtrl',
          //data : { requiresAuth : true},
          resolve  : {
            workflows : function(orchestraServer){
              return orchestraServer.getMetaWorkflows();
            }

          }
        })

        .state('workflows', {
          url: "/workflows",
          templateUrl: "templates/workflows.html",
          controller  :'WfCtrl',
          //data : { requiresAuth : true},
          resolve  : {
            workflows : function(orchestraServer){
              return orchestraServer.getWorkflows();
            }

          }
        })

        .state('login', {
          url: "/login",
          templateUrl: "templates/login.html",
          data : { requiresAuth : true}
        });

    }

  ])


  
  
  .run(function ($rootScope, AUTH_EVENTS, DrfAuthService) {

      $rootScope.$on('$stateChangeStart', function (event, next) {

          if(!next.data){
            return;
          }

          if(next.data.requiresAuth){
            if (!DrfAuthService.isAuthenticated()) {
              // user is not allowed
              event.preventDefault();
              $rootScope.$broadcast(AUTH_EVENTS.notAuthenticated);
            }
            
          }


          var authorizedRoles = next.data.authorizedRoles;
          if(authorizedRoles){
            if (!DrfAuthService.isAuthorized(authorizedRoles)) {
                event.preventDefault();
            if (DrfAuthService.isAuthenticated()) {
                // user is not allowed
                $rootScope.$broadcast(AUTH_EVENTS.notAuthorized);
            } else {
              // user is not logged in
              $rootScope.$broadcast(AUTH_EVENTS.notAuthenticated);
            }
          }
      }
  });

})



}())
