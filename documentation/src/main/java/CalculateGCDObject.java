import lsfusion.server.data.sql.exception.SQLHandledException;
import lsfusion.server.data.value.DataObject;
import lsfusion.server.language.ScriptingErrorLog;
import lsfusion.server.language.ScriptingLogicsModule;
import lsfusion.server.logics.action.controller.context.ExecutionContext;
import lsfusion.server.logics.classes.ValueClass;
import lsfusion.server.logics.property.classes.ClassPropertyInterface;
import lsfusion.server.physics.dev.integration.internal.to.InternalAction;

import java.math.BigInteger;
import java.sql.SQLException;

public class CalculateGCDObject extends InternalAction {

    public CalculateGCDObject(ScriptingLogicsModule LM, ValueClass... classes) {
        super(LM, classes);
    }

    @Override
    protected void executeInternal(ExecutionContext<ClassPropertyInterface> context) throws SQLException, SQLHandledException {
        try {
            DataObject calculation = (DataObject)getParamValue(0, context);
            BigInteger b1 = BigInteger.valueOf((Integer)findProperty("a").read(context, calculation));
            BigInteger b2 = BigInteger.valueOf((Integer)findProperty("b").read(context, calculation));
            BigInteger gcd = b1.gcd(b2);
            findProperty("gcd[Calculation]").change(gcd.intValue(), context, calculation);
        } catch (ScriptingErrorLog.SemanticErrorException ignored) {
        }
    }
}
