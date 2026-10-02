import java.io.*;
import java.nio.file.*;
import java.util.*;

public class TicketAnalyzer {

    static class Ticket {
        String ticketId;
        String department;
        String category;
        String priority;
        String technician;
        String status;
        double resolutionHours;

        Ticket(String ticketId, String department, String category, String priority,
               String technician, String status, double resolutionHours) {
            this.ticketId = ticketId;
            this.department = department;
            this.category = category;
            this.priority = priority;
            this.technician = technician;
            this.status = status;
            this.resolutionHours = resolutionHours;
        }
    }

    private static final List<Ticket> tickets = new ArrayList<>();

    public static void main(String[] args) {
        String filePath = "data/processed/it_tickets_clean.csv";

        try {
            loadTickets(filePath);
            System.out.println("Loaded " + tickets.size() + " tickets.");

            Scanner scanner = new Scanner(System.in);
            int choice;

            do {
                printMenu();
                System.out.print("Choose an option: ");
                choice = readInt(scanner);

                switch (choice) {
                    case 1 -> showTicketCountByCategory();
                    case 2 -> showAverageResolutionByPriority();
                    case 3 -> showOpenBacklog();
                    case 4 -> showTechnicianSummary();
                    case 5 -> System.out.println("Exiting Ticket Analyzer.");
                    default -> System.out.println("Invalid option. Try again.");
                }
            } while (choice != 5);

        } catch (IOException e) {
            System.out.println("Could not read ticket file: " + e.getMessage());
        }
    }

    static void loadTickets(String filePath) throws IOException {
        List<String> lines = Files.readAllLines(Paths.get(filePath));

        for (int i = 1; i < lines.size(); i++) {
            String[] parts = parseCsvLine(lines.get(i));

            if (parts.length < 17) {
                continue;
            }

            String ticketId = parts[0];
            String department = parts[2];
            String category = parts[4];
            String priority = parts[5];
            String technician = parts[6];
            String status = parts[9];

            double resolutionHours = 0.0;
            if (!parts[8].isBlank()) {
                try {
                    resolutionHours = Double.parseDouble(parts[8]);
                } catch (NumberFormatException ignored) {
                }
            }

            tickets.add(new Ticket(
                    ticketId,
                    department,
                    category,
                    priority,
                    technician,
                    status,
                    resolutionHours
            ));
        }
    }

    static String[] parseCsvLine(String line) {
        List<String> values = new ArrayList<>();
        StringBuilder current = new StringBuilder();
        boolean insideQuotes = false;

        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);

            if (c == '"') {
                insideQuotes = !insideQuotes;
            } else if (c == ',' && !insideQuotes) {
                values.add(current.toString());
                current.setLength(0);
            } else {
                current.append(c);
            }
        }

        values.add(current.toString());
        return values.toArray(new String[0]);
    }

    static void printMenu() {
        System.out.println("\n=== IT Service Ticket Analyzer ===");
        System.out.println("1. Ticket count by category");
        System.out.println("2. Average resolution time by priority");
        System.out.println("3. Open ticket backlog");
        System.out.println("4. Technician summary");
        System.out.println("5. Exit");
    }

    static int readInt(Scanner scanner) {
        while (!scanner.hasNextInt()) {
            System.out.print("Enter a number: ");
            scanner.next();
        }
        int value = scanner.nextInt();
        scanner.nextLine();
        return value;
    }

    static void showTicketCountByCategory() {
        Map<String, Integer> counts = new TreeMap<>();

        for (Ticket ticket : tickets) {
            counts.put(ticket.category, counts.getOrDefault(ticket.category, 0) + 1);
        }

        System.out.println("\nTickets by Category");
        for (Map.Entry<String, Integer> entry : counts.entrySet()) {
            System.out.printf("%-20s %d%n", entry.getKey(), entry.getValue());
        }
    }

    static void showAverageResolutionByPriority() {
        Map<String, Double> totals = new TreeMap<>();
        Map<String, Integer> counts = new TreeMap<>();

        for (Ticket ticket : tickets) {
            if ((ticket.status.equals("Closed") || ticket.status.equals("Resolved"))
                    && ticket.resolutionHours > 0) {
                totals.put(ticket.priority,
                        totals.getOrDefault(ticket.priority, 0.0) + ticket.resolutionHours);
                counts.put(ticket.priority,
                        counts.getOrDefault(ticket.priority, 0) + 1);
            }
        }

        System.out.println("\nAverage Resolution Time by Priority");
        for (String priority : totals.keySet()) {
            double average = totals.get(priority) / counts.get(priority);
            System.out.printf("%-10s %.2f hours%n", priority, average);
        }
    }

    static void showOpenBacklog() {
        Map<String, Integer> backlog = new TreeMap<>();

        for (Ticket ticket : tickets) {
            if (ticket.status.equals("Open") || ticket.status.equals("In Progress")) {
                backlog.put(ticket.priority,
                        backlog.getOrDefault(ticket.priority, 0) + 1);
            }
        }

        System.out.println("\nOpen Backlog by Priority");
        for (Map.Entry<String, Integer> entry : backlog.entrySet()) {
            System.out.printf("%-10s %d%n", entry.getKey(), entry.getValue());
        }
    }

    static void showTechnicianSummary() {
        Map<String, Integer> closedCounts = new TreeMap<>();
        Map<String, Double> hours = new TreeMap<>();

        for (Ticket ticket : tickets) {
            if (ticket.status.equals("Closed") || ticket.status.equals("Resolved")) {
                closedCounts.put(ticket.technician,
                        closedCounts.getOrDefault(ticket.technician, 0) + 1);
                hours.put(ticket.technician,
                        hours.getOrDefault(ticket.technician, 0.0) + ticket.resolutionHours);
            }
        }

        System.out.println("\nTechnician Summary");
        System.out.printf("%-15s %-15s %-20s%n",
                "Technician", "Tickets Closed", "Avg Resolution Hours");

        for (String technician : closedCounts.keySet()) {
            double avg = hours.get(technician) / closedCounts.get(technician);
            System.out.printf("%-15s %-15d %.2f%n",
                    technician, closedCounts.get(technician), avg);
        }
    }
}
