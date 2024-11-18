class ServicePostgres:
    async def selectUser(self, req, value):
        try:
            async with req.app.async_pool.connection() as conn:
                async with conn.cursor() as cur:
                    await cur.execute(
                        """
                        SELECT * 
                        FROM Core.Identities
                        WHERE user_id = %s
                    """,
                        [value]
                    )
                    results = await cur.fetchall()
                    return {"user_id": str(results[0][0]), "permissions": results[0][1]}
                    
        except Exception:
            pass
