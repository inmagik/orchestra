(function(){

'use strict';

angular.module('OrchestraServer', [])

.factory('orchestraServer', ['$http', '$q', function($http, $q) {
    
    
    var svc = {};
    svc.baseUrl = "http://localhost:8000/"

    svc.getMetaWorkflows = function(){
        var deferred = $q.defer();

        var data = ["this", "is", "a", "test"];

        console.log(data)

        
        var url = svc.baseUrl + "api/workflows/"
        $http.get(url).then(function(resp){
            deferred.resolve(resp.data);
        })

        return deferred.promise;

    }


    return svc;





}]);






})();