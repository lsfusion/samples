import lsfusion.interop.action.ClientAction;
import lsfusion.interop.action.ClientActionDispatcher;

import java.awt.*;
import java.io.IOException;

public class ClientBeep implements ClientAction {
    
    int times;

    public ClientBeep(int times) {
        this.times = times;
    }

    @Override
    public Object dispatch(ClientActionDispatcher dispatcher) throws IOException {
        for (int i = 0; i < times; i++) {
            try {
                Thread.sleep(1000);
                Toolkit.getDefaultToolkit().beep();
            } catch (InterruptedException ignored) {
            }
        }
        return "succeed";
    }
}
