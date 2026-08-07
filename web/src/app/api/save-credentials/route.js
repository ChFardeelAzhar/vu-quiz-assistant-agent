import { NextResponse } from 'next/server';
import crypto from 'crypto';
import { createServerClient } from '@supabase/ssr';
import { cookies } from 'next/headers';

const ENCRYPTION_KEY = process.env.ENCRYPTION_KEY || 'default_secret_key_32_bytes_long!'; // Must be 32 bytes
const ALGORITHM = 'aes-256-cbc';

function encrypt(text) {
  const iv = crypto.randomBytes(16);
  const cipher = crypto.createCipheriv(ALGORITHM, Buffer.from(ENCRYPTION_KEY), iv);
  let encrypted = cipher.update(text);
  encrypted = Buffer.concat([encrypted, cipher.final()]);
  return iv.toString('hex') + ':' + encrypted.toString('hex');
}

export async function POST(request) {
  try {
    const { vuId, vuPassword } = await request.json();

    if (!vuId || !vuPassword) {
      return NextResponse.json({ error: 'VU ID and Password are required' }, { status: 400 });
    }

    const cookieStore = await cookies();
    const supabase = createServerClient(
      process.env.NEXT_PUBLIC_SUPABASE_URL,
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY,
      {
        cookies: {
          getAll() { return cookieStore.getAll() },
          setAll() {},
        }
      }
    );

    const { data: { user }, error: authError } = await supabase.auth.getUser();

    if (authError || !user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Encrypt the LMS Password
    const encryptedPassword = encrypt(vuPassword);

    // Save to Supabase (profiles table)
    // NOTE: This assumes you have a 'profiles' table with 'id', 'vu_id', and 'vu_password_encrypted' columns.
    const { error: dbError } = await supabase
      .from('profiles')
      .upsert({ 
        id: user.id, 
        vu_id: vuId, 
        vu_password_encrypted: encryptedPassword,
        updated_at: new Date().toISOString()
      });

    if (dbError) {
      console.error('Database Error:', dbError);
      return NextResponse.json({ error: 'Failed to save to database. Make sure you created the profiles table in Supabase.' }, { status: 500 });
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Server Error:', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}
