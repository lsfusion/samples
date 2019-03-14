import com.google.common.base.Throwables;
import lsfusion.server.language.ScriptingAction;
import lsfusion.server.logics.classes.ValueClass;
import lsfusion.server.data.SQLHandledException;
import lsfusion.server.data.DataObject;
import lsfusion.server.logics.property.classes.ClassPropertyInterface;
import lsfusion.server.logics.action.ExecutionContext;
import lsfusion.server.language.ScriptingLogicsModule;

import java.lang.ref.WeakReference;
import java.sql.SQLException;
import java.util.Iterator;

public class KillProcessActionProperty extends ScriptingAction {
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
