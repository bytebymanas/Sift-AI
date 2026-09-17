import { NextResponse } from 'next/server';

export async function POST() {
  const { GITHUB_PAT_TOKEN, REPO_OWNER, REPO_NAME } = process.env;

  if (!GITHUB_PAT_TOKEN || !REPO_OWNER || !REPO_NAME) {
    return NextResponse.json(
      { error: 'Required environment variables missing on Vercel.' },
      { status: 500 }
    );
  }

  try {
    const res = await fetch(
      `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/dispatches`,
      {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${GITHUB_PAT_TOKEN}`,
          Accept: 'application/vnd.github.v3+json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ event_type: 'trigger_colab_run' }),
      }
    );

    if (res.ok) {
      return NextResponse.json({ status: 'Dispatched successfully' });
    }

    const details = await res.text();
    return NextResponse.json({ error: details }, { status: res.status });
  } catch (err) {
    return NextResponse.json({ error: err.message }, { status: 500 });
  }
}