def addition(numbers: list) -> float:
    return sum(numbers)
def show_code():
    code = '''
//restapplication
package mileToKm;
import javax.ws.rs.ApplicationPath;
import javax.ws.rs.core.Application;
@ApplicationPath("/api")
public class RestApplication extends Application {
    
}
//MileToKmRestService
package mileToKm;
import javax.ws.rs.GET;
import javax.ws.rs.Path;
import javax.ws.rs.QueryParam;
@Path("/converter") // This sets the path for this service to /api/converter
public class MileToKmRestService {
 @GET
 @Path("/mileToKm") // This sets the path for this specific method
 public String convertMileToKm(@QueryParam("miles") double miles) {
 double km = miles * 1.60934; // Conversion logic: 1 mile = 1.60934 km
 return miles + " miles = " + km + " kilometers";
 }
}
    '''
    print(code)