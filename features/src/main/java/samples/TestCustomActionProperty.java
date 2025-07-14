package samples;

import com.google.common.base.Throwables;
import lsfusion.server.language.ScriptingLogicsModule;
import lsfusion.server.logics.action.controller.context.ExecutionContext;
import lsfusion.server.logics.property.classes.ClassPropertyInterface;
import lsfusion.server.physics.dev.integration.internal.to.InternalAction;

public class TestCustomActionProperty extends InternalAction {

    public TestCustomActionProperty(ScriptingLogicsModule LM) {
        super(LM);
    }

    @Override
    protected void executeInternal(ExecutionContext<ClassPropertyInterface> context) {

        try {
            new YandexLabelByDate().search();
        } catch (Exception e) {
            throw Throwables.propagate(e);
        }


        System.out.println("hi");
    }
}
