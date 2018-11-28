import com.google.common.base.Throwables;
import lsfusion.server.classes.ValueClass;
import lsfusion.server.data.SQLHandledException;
import lsfusion.server.logics.DataObject;
import lsfusion.server.logics.linear.LCP;
import lsfusion.server.logics.property.ClassPropertyInterface;
import lsfusion.server.logics.property.ExecutionContext;
import lsfusion.server.logics.scripted.ScriptingActionProperty;
import lsfusion.server.logics.scripted.ScriptingLogicsModule;

import java.io.File;
import java.io.InputStream;
import java.lang.ref.WeakReference;
import java.sql.SQLException;
import java.util.Iterator;
import java.util.concurrent.ConcurrentHashMap;

public class KillProcessActionProperty extends ScriptingActionProperty {
    private final ClassPropertyInterface serverInterface;

    public KillProcessActionProperty(ScriptingLogicsModule LM, ValueClass... classes) {
        super(LM, classes);

        Iterator<ClassPropertyInterface> i = interfaces.iterator();
        serverInterface = i.next();
    }

    @Override
    public void executeCustom(ExecutionContext<ClassPropertyInterface> context) throws SQLException, SQLHandledException {
        DataObject server = (DataObject) context.getKeyValue(serverInterface);

        try {
            WeakReference<Process> weakProcess = RunProcessActionProperty.runningProcesses.get((Long) server.object);
            Process p;
            if(weakProcess != null && (p = weakProcess.get()) != null) {
                p.destroy();
            }                
        } catch (Exception e) {
            throw Throwables.propagate(e);
        }
    }
}
