import sqlite3
DB_PATH = "creditos.db" #Se va a crear al ejecutar el codigo app.py

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn

def ini_db(): 
    """ Crea la tabla creditos """
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS creditos (
                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                     cliente TEXT NOT NULL,
                     monto REAL NOT NULL,
                     tasa_interes REAL NOT NULL,
                     plazo INTEGER NOT NULL,
                     fecha_otorgamiento TEXT NOT NULL
                     )
                """)
        
def create_credito(cliente, monto, tasa_interes, plazo, fecha_otorgamiento):
    """ Inserta un nuevo credito y regresa su id """
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO creditos (cliente, monto, tasa_interes, plazo, fecha_otorgamiento) VALUES (?,?,?,?,?)",
            (cliente, monto, tasa_interes, plazo, fecha_otorgamiento)
        )
        return cursor.lastrowid
    
def get_all_creditos():
    """Devuelve la lista de creditos"""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM creditos ORDER BY fecha_otorgamiento")
        rows = cur.fetchall()
    return[dict(r) for r in rows]

def get_credito(credito_id):
    """Busca por id"""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM creditos WHERE id = ?", (credito_id,))
        row = cur.fetchone()
    return dict(row) if row else None

def update_credito(credito_id, cliente, monto, tasa_interes, plazo, fecha_otorgamiento):
    """Actualiza"""
    with get_connection() as conn:
        cur = conn.execute("""
                           UPDATE creditos
                           SET cliente=?, monto=?, tasa_interes=?, plazo=?, fecha_otorgamiento=?
                           WHERE id=?
                           """, (cliente, monto, tasa_interes, plazo, fecha_otorgamiento, credito_id))
        
        return cur.rowcount
    
def delete_credito(credito_id):
    """Elimina"""
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM creditos WHERE id=?", (credito_id,))

        return cur.rowcount

#-----------Funciones para Graficas----------

def get_total_month():
    """Devuelve lista agregada por mes"""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT substr(fecha_otorgamiento,1,7) AS mes, SUM(monto) AS total
            FROM creditos
            GROUP BY mes
            ORDER BY mes
        """)
        rows = cur.fetchall()
    
    return [{"mes": r["mes"] or "sin_fecha", "total": r["total"] or 0} for r in rows]

def get_total_cliente():
    """Devuelve la lista agregada por clientes"""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT cliente, SUM(monto) AS total
            FROM creditos
            GROUP BY cliente
            ORDER BY total DESC
         """)
        rows = cur.fetchall()
    
    return [{"cliente": r["cliente"], "total": r["total"] or 0} for r in rows]

def get_distribucion_ranges(ranges):
    """
    ranges: lista de tuples (min, max) o (min, None)
    Devuelve lista {'label': '0-10000', 'total': monto}
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT monto FROM creditos")
        rows = cur.fetchall()

    montos = [float(r["monto"]) for r in rows]
    buckets = []
    for lo, hi in ranges:
        if hi is None:
            label = f">{lo}"
            total = sum (m for m in montos if m > lo)
        else:
            label = f"{lo}-{hi}"
            total = sum (m for m in montos if lo <= m <= hi)
        buckets.append({"label": label, "total": total})

    return buckets