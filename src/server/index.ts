import express from "express";
import cors from "cors";
import path from "path";
import userRoutes from "./routes/users";
import groupRoutes from "./routes/groups";
import expenseRoutes from "./routes/expenses";
import settlementRoutes from "./routes/settlements";

const app = express();
const PORT = process.env.PORT || 3001;

app.use(cors());
app.use(express.json());

// API routes
app.use("/api/users", userRoutes);
app.use("/api/groups", groupRoutes);
app.use("/api/expenses", expenseRoutes);
app.use("/api/settlements", settlementRoutes);

// Serve static files in production
const clientBuildPath = path.join(__dirname, "..", "..", "client", "build");
app.use(express.static(clientBuildPath));
app.get("*", (_req, res) => {
  res.sendFile(path.join(clientBuildPath, "index.html"));
});

app.listen(Number(PORT), "0.0.0.0", () => {
  console.log(`Server running on http://0.0.0.0:${PORT}`);
});

export default app;
