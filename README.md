
# KnowledgeAcquisition

---

 1. Install the aidalight source code on your university session (http://download.mpi-inf.mpg.de/d5/aida/aidalight.zip)
 2. Replace the content of the AIDALight_client.java file located in the directory **src/mpi/aidalight/rmi/** by this code :  
```java
package mpi.aidalight.rmi;

import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;
import java.util.List;
import java.util.Map;

import mpi.aida.data.Entity;
import mpi.aida.data.Mention;


public class AIDALight_client {
  
  /**
   * 
   * @param text - this is clean text.
   * @param mentions: set null if mentions are not annotated. In this case, StanfordNER will be used to annotate the text.
   * @throws RemoteException
   */
  public static void disambiguate(String text, List<Mention> mentions, String host) throws RemoteException {
    if(host == null)
      host = "x-aida-light.unicaen.fr"; // default
    
    System.out.println(host);
    // set up server
    AIDALightServer server = null;
    try {
      Registry registry = LocateRegistry.getRegistry(host, 52365);
      server = (AIDALightServer) registry.lookup("NEDServer_" + host);
    } catch (Exception e) {
      e.printStackTrace();
    }
    
    String command = "fullSettings"; // = key-words + 2-phase mapping + domain

    Map<Mention, Entity> annotations = server.disambiguate(text, mentions, command);
    
    // do whatever here...
    for(Mention mention: annotations.keySet()) {
      String wikipediaEntityId = "http://en.wikipedia.org/wiki/" + annotations.get(mention).getName();
      System.out.println(mention.getMention() + "\t" + wikipediaEntityId);
    }
  }
  
  public static void main(String args[]) throws Exception {
     AIDALight_client.disambiguate(args[0], null, null);
  }
}
```
3.  Recompile the aidalight source code by running this command at the root of the directory :  
`javac ./src/mpi/aidalight/rmi/AIDALight_client.java -cp ".:./bin:./lib/*" -d "./bin/"`
4. On your computer, download the PURE project and put it at the root of the current directory.
5. Edit run.py and add the following lines at the top of the file : 
``` 
    import sys
    import os
    os.chdir(os.getcwd() + '/PURE')
```

6. Follow the instructions of the file docker/README.txt 
7. Create a python virtual environment by running `python3 -m venv venv`
8. Install the python packages `pip install -r requirements.txt`
9. Run the flask application `flask run`

