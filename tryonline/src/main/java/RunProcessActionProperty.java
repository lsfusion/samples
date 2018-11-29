import com.google.common.base.Throwables;
import lsfusion.interop.action.MessageClientAction;
import lsfusion.server.classes.ValueClass;
import lsfusion.server.data.SQLHandledException;
import lsfusion.server.logics.DataObject;
import lsfusion.server.logics.ObjectValue;
import lsfusion.server.logics.linear.LCP;
import lsfusion.server.logics.property.ClassPropertyInterface;
import lsfusion.server.logics.property.ExecutionContext;
import lsfusion.server.logics.scripted.ScriptingActionProperty;
import lsfusion.server.logics.scripted.ScriptingLogicsModule;
import lsfusion.utils.utils.RunCommandClientAction;

import java.io.BufferedInputStream;
import java.io.File;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.ref.WeakReference;
import java.sql.SQLException;
import java.util.Iterator;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.atomic.AtomicLong;

public class RunProcessActionProperty extends ScriptingActionProperty {
    private final ClassPropertyInterface serverInterface;
    private final ClassPropertyInterface commandInterface;
    private final ClassPropertyInterface directoryInterface;
    private final ClassPropertyInterface encodingInterface;

    public RunProcessActionProperty(ScriptingLogicsModule LM, ValueClass... classes) {
        super(LM, classes);

        Iterator<ClassPropertyInterface> i = getOrderInterfaces().iterator();
        serverInterface = i.next();
        commandInterface = i.next();
        directoryInterface = i.next();
        encodingInterface = i.next();
    }

    public static final ConcurrentHashMap<Long, WeakReference<Process>> runningProcesses = new ConcurrentHashMap<>();

    @Override
    public void executeCustom(ExecutionContext<ClassPropertyInterface> context) throws SQLException, SQLHandledException {
        String command = (String) context.getKeyValue(commandInterface).getValue();
        String directory = (String) context.getKeyValue(directoryInterface).getValue();
        DataObject server = (DataObject) context.getKeyValue(serverInterface);
        String encoding = (String) context.getKeyValue(encodingInterface).getValue();
        
        try {
            LCP<?> text = LM.findProperty("text[Server, LONG]");

            Process p = Runtime.getRuntime().exec(command, null, new File(directory));
            runningProcesses.put((Long) server.object, new WeakReference<>(p));
            
            long lastFlush = System.currentTimeMillis();
            long answerId = 0;
            StringBuilder outStringBuilder = new StringBuilder();
            byte[] b = new byte[10 * 1024];
            int bytesRead;
            InputStream out = p.getInputStream();
            while ((bytesRead = out.read(b)) != -1) {                
                outStringBuilder.append(new String(b, 0, bytesRead, encoding));
                long now = System.currentTimeMillis();
                if((now - lastFlush) > 100) {
                    outResult(context, server, text, answerId++, outStringBuilder.toString());
                    outStringBuilder = new StringBuilder();
                }                    
            }
            String outString = outStringBuilder.toString();
            if(!outString.isEmpty())
                outResult(context, server, text, answerId++, outString);

            int exitValue = p.exitValue();
            if(exitValue != 0) {
                InputStream error = p.getInputStream();
                StringBuilder errorStringBuilder = new StringBuilder();
                while ((bytesRead = error.read(b)) != -1)
                    errorStringBuilder.append(new String(b, 0, bytesRead, encoding));
                outResult(context, server, text, answerId, '\n' + "Process finished with error, exit code : " + exitValue + '\n' + errorStringBuilder.toString());
            }
        } catch (Exception e) {
            throw Throwables.propagate(e);
        }
    }

    public void outResult(ExecutionContext<ClassPropertyInterface> context, DataObject server, LCP<?> text, long answerId, String outString) throws SQLException, SQLHandledException {
        text.change(outString, context, server, new DataObject(answerId));
        context.applyException();
    }
}
