import ReverseModule.Reverse;
import org.omg.CosNaming.*;
import org.omg.CosNaming.NamingContextPackage.*;
import org.omg.CORBA.*;
import org.omg.PortableServer.*;
class ReverseServer
{
    public static void main(String[] args)
    {
        try{
            org.omg.CORBA.ORB orb = org.omg.CORBA.ORB.init(args,null);
            POA rootPOA = POAHelper.narrow(orb.resolve_initial_references("RootPOA"));
            rootPOA.the_POAManager().activate();
            ReverseImpl rvr = new ReverseImpl();
            org.omg.CORBA.Object ref = rootPOA.servant_to_reference(rvr);
            Reverse h_ref = ReverseModule.ReverseHelper.narrow(ref);
            org.omg.CORBA.Object objRef = orb.resolve_initial_references("NameService");
            NamingContextExt ncRef = NamingContextExtHelper.narrow(objRef);
            String name = "Reverse";
            NameComponent path[] = ncRef.to_name(name);
            ncRef.rebind(path,h_ref);
            System.out.println("Reverse Server reading and waiting....");
            orb.run();
        }
        catch(Exception e){
            e.printStackTrace();
        }
    }
}
