import { NextResponse } from "next/server";
import path from "path";
import sqlite3 from "sqlite3";
import { open } from "sqlite";

export async function GET() {
  try {
    // Resolve the clean backward path track into your memory-vault partition
    const dbPath = path.resolve(process.cwd(), "../memory-vault/project-instructions.db");

    // Initialize an isolated read-only storage stream hook
    const db = await open({
      filename: dbPath,
      driver: sqlite3.Database,
      mode: sqlite3.OPEN_READONLY,
    });

    // Extract table structural listings inside your instruction matrix
    const databaseSchema = await db.all("SELECT name FROM sqlite_master WHERE type='table';");
    
    await db.close();

    return NextResponse.json({
      status: "CONNECTED",
      target_resource: "project-instructions.db",
      tables: databaseSchema
    });
  } catch (error: any) {
    return NextResponse.json(
      { status: "SQLITE_IO_EXCEPTION", details: error.message },
      { status: 500 }
    );
  }
}