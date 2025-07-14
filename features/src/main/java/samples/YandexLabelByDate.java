package samples;

import com.sun.mail.iap.Argument;
import com.sun.mail.imap.IMAPFolder;
import com.sun.mail.imap.IMAPMessage;
import com.sun.mail.imap.IMAPStore;

import javax.mail.*;
import javax.mail.internet.InternetAddress;
import javax.mail.search.*;
import java.sql.Date;
import java.time.LocalDate;
import java.util.Arrays;
import java.util.Properties;

public class YandexLabelByDate {
    // --------------- КАНФІГУРАЦЫЯ ----------------
    private static final String HOST = "imap.yandex.ru";
    private static final int PORT = 993;
    private static final String USER = "vandrouny@tut.by";
    private static final String PASSWORD = "tczdisirfwgguyym";

    private static final String LABEL = "Люся7";  // ярлык
    private static final LocalDate DATE = LocalDate.of(2025, 6, 19); // шукаем па гэтай даце

    public static void search() throws Exception {

        Properties p = new Properties();
        p.put("mail.imap.ssl.enable", "true");
        Session s = Session.getInstance(p);

        try (IMAPStore st = (IMAPStore) s.getStore("imap")) {
            st.connect("imap.yandex.com", 993, USER, PASSWORD);   // стандартные IMAP‑параметры :contentReference[oaicite:2]{index=2}
            IMAPFolder f = (IMAPFolder) st.getFolder("INBOX");
            f.open(Folder.READ_ONLY);

            // 1. Собираем все UID
            Message[] msgs = f.getMessages();

            // 2. Говорим серверу выдать ярлыки
            FetchProfile fp = new FetchProfile();
            fp.add(IMAPFolder.FetchProfileItem.HEADERS);   // ← ключевой пункт
            f.fetch(msgs, fp);

/*            f.doCommand(protocol -> {
                // пример диапазона: 1:*  (все письма)  или  1:500
                Argument args = new Argument();
                args.writeAtom("UID");               // 1‑й атом
                args.writeAtom("FETCH");             // 2‑й
                args.writeAtom("1:*");               // 3‑й  (sequence‑set)
                Argument what = new Argument();      // вложенный список ()
                what.writeAtom("X-GM-LABELS");
                args.writeArgument(what);

                protocol.command("UID", args);       // отдаём как массив токенов
                return null;
            });*/

            // Ответ парсится listener’ом FolderEvent; проще – повторно пройтись по сообщениям
            for (Message m : msgs) {
                String[] labs = ((IMAPMessage) m).getHeader("X-GM-LABELS");
                if (labs != null)
                    System.out.println(Arrays.toString(labs));
            }
        }


        Properties props = new Properties();
        props.setProperty("mail.imap.ssl.enable", "true");
        props.setProperty("mail.store.protocol", "imap");

        Session session = Session.getInstance(props);
        Store store = session.getStore("imap");
        store.connect(HOST, PORT, USER, PASSWORD);

        // Адкрываем INBOX або іншую патрэбную папку
        Folder folder = store.getFolder("INBOX");
        folder.open(Folder.READ_ONLY);

        // Пераўтварэнне даты ў java.util.Date
        Date targetDate = java.sql.Date.valueOf(DATE);
        SearchTerm dateTerm = new ReceivedDateTerm(ComparisonTerm.EQ, targetDate);

        // Фільтр па загалоўку X-Yandex-Label
        SearchTerm labelTerm = new HeaderTerm("X-Yandex-Label", LABEL);

        // Аб’яднаем умовы: дата І ярлык
        SearchTerm compoundTerm = new AndTerm(dateTerm, labelTerm);

        Message[] messages = folder.search(dateTerm);
        System.out.printf("Знойдзена %d лістоў з ярлыкам '%s' за %s%n", messages.length, LABEL, DATE);

        for (Message msg : messages) {


            Address[] froms = msg.getFrom();
            String from = (froms != null && froms.length > 0) ? ((InternetAddress) froms[0]).getAddress() : "Невядомы";
            System.out.printf("➤ %s | ад: %s | %s%n",
                    msg.getReceivedDate(),
                    from,
                    msg.getSubject());
        }

        folder.close(false);
        store.close();
    }
}