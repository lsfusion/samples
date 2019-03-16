import com.google.common.base.Throwables;
import lsfusion.server.language.property.LP;
import lsfusion.server.logics.classes.ValueClass;
import lsfusion.server.data.sql.exception.SQLHandledException;
import lsfusion.server.data.value.DataObject;
import lsfusion.server.logics.property.classes.ClassPropertyInterface;
import lsfusion.server.logics.action.controller.context.ExecutionContext;
import lsfusion.server.physics.dev.integration.internal.to.InternalAction;
import lsfusion.server.language.ScriptingLogicsModule;

import java.io.File;
import java.io.InputStream;
import java.lang.ref.WeakReference;
import java.sql.SQLException;
import java.util.Iterator;
import java.util.concurrent.ConcurrentHashMap;

public class RunProcessActionProperty extends InternalAction {
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
    public void executeInternal(ExecutionContext<ClassPropertyInterface> context) throws SQLException, SQLHandledException {
        String command = (String) context.getKeyValue(commandInterface).getValue();
        String directory = (String) context.getKeyValue(directoryInterface).getValue();
        DataObject server = (DataObject) context.getKeyValue(serverInterface);
        String encoding = (String) context.getKeyValue(encodingInterface).getValue();
        
        try {
            LP<?> text = LM.findProperty("text[Server, LONG]");

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
            int exitValue = p.waitFor();
            if(exitValue != 0) {
                outStringBuilder.append("Process finished with error, exit code : ").append(exitValue).append('\n');

                InputStream error = p.getErrorStream();
                while ((bytesRead = error.read(b)) != -1)
                    outStringBuilder.append(new String(b, 0, bytesRead, encoding));
            }

            String outString = outStringBuilder.toString();
            if(!outString.isEmpty())
                outResult(context, server, text, answerId++, outString);
        } catch (Exception e) {
            throw Throwables.propagate(e);
        }
    }

    public void outResult(ExecutionContext<ClassPropertyInterface> context, DataObject server, LP<?> text, long answerId, String outString) throws SQLException, SQLHandledException {
        text.change(outString, context, server, new DataObject(answerId));
        context.applyException();
    }
}
