import lsfusion.server.data.sql.exception.SQLHandledException;
import lsfusion.server.language.ScriptingErrorLog;
import lsfusion.server.language.ScriptingLogicsModule;
import lsfusion.server.logics.action.controller.context.ExecutionContext;
import lsfusion.server.logics.classes.ValueClass;
import lsfusion.server.logics.property.classes.ClassPropertyInterface;
import lsfusion.server.physics.dev.integration.internal.to.InternalAction;

import java.math.BigInteger;
import java.sql.SQLException;

public class CalculateGCD extends InternalAction {

    public CalculateGCD(ScriptingLogicsModule LM, ValueClass... classes) {
        super(LM, classes);
    }

    @Override
    protected void executeInternal(ExecutionContext<ClassPropertyInterface> context) throws SQLException, SQLHandledException {
        BigInteger a = BigInteger.valueOf((Integer)getParam(0, context));
        BigInteger b = BigInteger.valueOf((Integer)getParam(1, context));
        BigInteger gcd = a.gcd(b);
        try {
            findProperty("gcd[]").change(gcd.intValue(), context);
        } catch (ScriptingErrorLog.SemanticErrorException ignored) {
        }
    }
}
