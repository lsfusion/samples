import com.google.common.base.Throwables;
import lsfusion.server.data.value.DataObject;
import lsfusion.server.language.ScriptingLogicsModule;
import lsfusion.server.logics.action.controller.context.ExecutionContext;
import lsfusion.server.logics.classes.ValueClass;
import lsfusion.server.logics.property.classes.ClassPropertyInterface;
import lsfusion.server.physics.dev.integration.internal.to.InternalAction;

import java.lang.ref.WeakReference;
import java.util.Iterator;

public class KillProcessActionProperty extends InternalAction {
    private final ClassPropertyInterface serverInterface;

    public KillProcessActionProperty(ScriptingLogicsModule LM, ValueClass... classes) {
        super(LM, classes);

        Iterator<ClassPropertyInterface> i = interfaces.iterator();
        serverInterface = i.next();
    }

    @Override
    public void executeInternal(ExecutionContext<ClassPropertyInterface> context) {
        DataObject server = (DataObject) context.getKeyValue(serverInterface);

        try {
            WeakReference<Process> weakProcess = RunProcessActionProperty.runningProcesses.get(server.object);
            Process p;
            if(weakProcess != null && (p = weakProcess.get()) != null) {
                p.destroy();
            }                
        } catch (Exception e) {
            throw Throwables.propagate(e);
        }
    }
}
