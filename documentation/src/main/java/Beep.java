import lsfusion.server.language.ScriptingLogicsModule;
import lsfusion.server.logics.action.controller.context.ExecutionContext;
import lsfusion.server.logics.property.classes.ClassPropertyInterface;
import lsfusion.server.physics.dev.integration.internal.to.InternalAction;

public class Beep extends InternalAction {

    public Beep(ScriptingLogicsModule LM) {
        super(LM);
    }

    @Override
    protected void executeInternal(ExecutionContext<ClassPropertyInterface> context) {
        String result = (String) context.requestUserInteraction(new ClientBeep(5));
        System.out.println(result);
    }
}
