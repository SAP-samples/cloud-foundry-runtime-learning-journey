using my.bookshop as my from '../db/data-model';

service CatalogService @(requires: 'any') {
    @readonly
    entity Books as projection on my.Books
    // Application Autoscaler - Unbound Function
    function useCPU(action : String, duration : String) returns String;

}
