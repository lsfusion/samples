import lsfusion.server.data.sql.exception.SQLHandledException;
import lsfusion.server.language.ScriptingErrorLog;
import lsfusion.server.language.ScriptingLogicsModule;
import lsfusion.server.logics.action.controller.context.ExecutionContext;
import lsfusion.server.logics.property.classes.ClassPropertyInterface;
import lsfusion.server.physics.dev.integration.internal.to.InternalAction;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.sql.SQLException;

public class GetIP extends InternalAction {

    public GetIP(ScriptingLogicsModule LM) {
        super(LM);
    }

    @Override
    protected void executeInternal(ExecutionContext<ClassPropertyInterface> context) throws SQLException, SQLHandledException {
        try {
            findProperty("ip").change(InetAddress.getLocalHost().toString(), context);
        } catch (UnknownHostException | ScriptingErrorLog.SemanticErrorException ignored) {}        
    }
}
